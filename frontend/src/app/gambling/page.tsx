import React from 'react';
import Link from 'next/link'; // Restoring the correct Next.js Link component

export default function GamblingPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900 text-white">
      <div className="text-center">
        <h1 className="text-5xl font-bold mb-4">Gambling Home</h1>
        <p className="text-xl text-gray-400 mb-8">
          This section is under construction.
        </p>
        <Link 
          href="/"
          className="rounded-lg border border-transparent px-5 py-3 transition-colors duration-300 bg-gray-700 text-white hover:bg-gray-600 hover:border-gray-500"
        >
          ← Go Back Home
        </Link>
      </div>
    </main>
  );
}
