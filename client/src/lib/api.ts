const base = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.API_BASE_URL || 'http://localhost:4001';

export async function api(path: string, init?: RequestInit) {
  const res = await fetch(`${base}${path}`, { 
    ...init, 
    headers: { 
      'Content-Type': 'application/json', 
      ...(init?.headers||{}) 
    }
  });
  
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`[API] ${res.status} ${text}`);
  }
  
  return res.json();
}

