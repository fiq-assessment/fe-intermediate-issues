from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import random

app = FastAPI(title="Issue Tracker Mock API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory mock data
STATUSES = ["open", "in_progress", "resolved", "closed"]
PRIORITIES = ["low", "medium", "high", "critical"]
TICKETS = []

# Generate mock tickets
TITLES = [
    "Login page not responding",
    "Dashboard loading slowly",
    "Payment gateway timeout",
    "Email notifications not sent",
    "Search functionality broken",
    "Profile image upload fails",
    "API rate limiting issues",
    "Database connection errors",
    "Mobile UI rendering problems",
    "Export to CSV not working"
]

for i in range(1, 51):
    TICKETS.append({
        "id": str(i),
        "title": random.choice(TITLES) + f" #{i}",
        "description": f"Detailed description of issue {i}. This explains the problem, steps to reproduce, and expected vs actual behavior.",
        "status": random.choice(STATUSES),
        "priority": random.choice(PRIORITIES),
        "createdAt": (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()
    })

class StatusUpdate(BaseModel):
    status: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/tickets")
async def list_tickets(
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = 20
):
    """
    EXPECTATION:
    - Implement offset pagination.
    - Filter by search term (title/description).
    - Support sorting by created_at, priority, status.
    """
    filtered = TICKETS.copy()
    
    if search:
        search_lower = search.lower()
        filtered = [t for t in filtered if search_lower in t["title"].lower() or search_lower in t["description"].lower()]
    
    # Sort
    if sort:
        key, direction = sort.split(":") if ":" in sort else (sort, "desc")
        reverse = (direction == "desc")
        
        if key == "created_at":
            filtered.sort(key=lambda x: x["createdAt"], reverse=reverse)
        elif key == "priority":
            priority_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
            filtered.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=reverse)
        elif key == "status":
            filtered.sort(key=lambda x: x["status"], reverse=reverse)
    else:
        filtered.sort(key=lambda x: x["createdAt"], reverse=True)
    
    # Paginate
    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    items = filtered[start:end]
    
    total_pages = max(1, (total + limit - 1) // limit)
    
    return {
        "items": items,
        "page": page,
        "totalPages": total_pages,
        "total": total
    }

@app.patch("/tickets/{id}")
async def update_ticket_status(id: str, update: StatusUpdate):
    """
    EXPECTATION:
    - Update ticket status.
    - Return 404 if not found.
    - Validate status value.
    """
    if update.status not in STATUSES:
        raise HTTPException(400, "Invalid status")
    
    ticket = next((t for t in TICKETS if t["id"] == id), None)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    
    # Simulate occasional failure for testing rollback
    if random.random() < 0.1:  # 10% chance of failure
        raise HTTPException(500, "Simulated server error")
    
    ticket["status"] = update.status
    return ticket

