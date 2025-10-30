import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="container">
      <div className="card">
        <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>FE Intermediate: Issue Tracker</h1>
        <p style={{ marginBottom: '1rem' }}>
          Build an issue tracker with optimistic updates, server-side pagination, and filtering.
        </p>
        <Link href="/tickets" className="btn">
          Go to Tickets →
        </Link>
      </div>
    </div>
  );
}

