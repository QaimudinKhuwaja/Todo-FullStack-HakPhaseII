"use client"; // This is a client component

import { useEffect, useState } from 'react';

export default function HealthPage() {
  const [status, setStatus] = useState('Loading...');

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch('http://localhost:8000/health'); // Assuming backend runs on 8000
        const data = await response.json();
        setStatus(data.status);
      } catch (error) {
        setStatus('Error: Could not connect to backend.');
        console.error('Error fetching health status:', error);
      }
    }
    fetchHealth();
  }, []);

  return (
    <div>
      <h1>Backend Health Status</h1>
      <p>Status: {status}</p>
    </div>
  );
}
