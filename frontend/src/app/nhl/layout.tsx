import React from 'react';
// This path is now correct: from /src/app/nhl/ it goes up to /src/app/
// and then into /src/app/components/Sidebar
import Sidebar from '../components/Sidebar'; 

export default function NhlLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-gray-900 text-gray-100">
      <Sidebar />
      <main className="flex-1 p-4 sm:p-8">
        {children}
      </main>
    </div>
  );
}
