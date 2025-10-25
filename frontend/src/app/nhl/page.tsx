import React from 'react';
import Link from 'next/link';

// Helper component for the navigation cards
const InfoCard = ({ title, description, href }: { title: string, description: string, href: string }) => (
  <Link 
    href={href}
    className="group rounded-lg border border-transparent px-5 py-4 transition-all duration-300 ease-in-out bg-gray-800 border-gray-700 hover:bg-gray-700/80 hover:border-gray-500 transform hover:-translate-y-1 hover:shadow-lg"
  >
    <h2 className="mb-3 text-2xl font-semibold text-white">
      {title}
      <span className="inline-block transition-transform duration-300 group-hover:translate-x-1 motion-reduce:transform-none">
        &nbsp;→
      </span>
    </h2>
    <p className="m-0 max-w-[30ch] text-sm text-gray-300 opacity-90">
      {description}
    </p>
  </Link>
);

// This is the main Home Page component
export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-900 text-white">
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4">BirdPicks</h1>
        <p className="text-xl text-gray-400">NHL Data Analysis & Predictions</p>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <InfoCard
          href="/gambling"
          title="Gambling Home"
          description="View gambling analytics, models, and tools."
        />

        <InfoCard
          href="/nhl"
          title="NHL"
          description="Explore NHL schedules, stats, and player data."
        />
      </div>
    </main>
  );
}
