'use client'; 

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

// Define the ScheduleItem type
type ScheduleItem = {
  id: number;
  date: string;
  time: string;
  visitor: string;
  home: string;
  visitor_goals: number | null;
  home_goals: number | null;
  attendance: number | null;
  notes: string | null;
};

// Helper function to get today's date in 'YYYY-MM-DD' format (in UTC)
const getTodayUTCString = () => {
  const today = new Date();
  // Note: Using UTC to match the server/database timezone logic
  const year = today.getUTCFullYear();
  const month = String(today.getUTCMonth() + 1).padStart(2, '0');
  const day = String(today.getUTCDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// Helper to format time
const formatTime = (timeString: string) => {
  if (!timeString) return 'TBD';
  const parts = timeString.split(':');
  if (parts.length < 2) return 'Invalid Time';
  
  const [hours, minutes] = parts;
  const date = new Date();
  date.setHours(parseInt(hours), parseInt(minutes));
  return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
};

// This is the main component for your NHL dashboard page
export default function NhlDashboardPage() {
  const [todaysGames, setTodaysGames] = useState<ScheduleItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await fetch('http://localhost:8000/schedule/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const allGames: ScheduleItem[] = await response.json();
        
        // Filter for today's games
        const todayString = getTodayUTCString();
        const filteredGames = allGames.filter(game => game.date === todayString);
        
        setTodaysGames(filteredGames);
      } catch (e) {
        if (e instanceof Error) {
            setError(`Failed to fetch schedule data: ${e.message}`);
        } else {
            setError("An unknown error occurred.");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchSchedule();
  }, []);

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="text-center p-10">
          <h2 className="text-2xl font-semibold">Loading Today's Games...</h2>
        </div>
      );
    }

    if (error) {
      return (
        <div className="text-center p-10 bg-red-900/20 border border-red-700 rounded-lg">
          <h2 className="text-2xl font-semibold text-red-400">Error</h2>
          <p className="mt-2 text-red-300">{error}</p>
        </div>
      );
    }

    if (todaysGames.length === 0) {
      return (
        <div className="text-center p-10 bg-gray-800/50 border border-gray-700 rounded-lg">
          <h2 className="text-2xl font-semibold">No Games Today</h2>
          <p className="mt-2 text-gray-400">There are no games scheduled for today.</p>
          <Link 
            href="/nhl/schedule"
            className="mt-4 inline-block rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 transition-colors"
          >
            View Full Schedule
          </Link>
        </div>
      );
    }

    return (
      <div className="overflow-x-auto rounded-lg border border-gray-700">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-800">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Time</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Away Team</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Home Team</th>
              <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Score</th>
            </tr>
          </thead>
          <tbody className="bg-gray-800/50 divide-y divide-gray-700">
            {todaysGames.map((game) => (
              <tr key={game.id} className="hover:bg-gray-700/50 transition-colors duration-200">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{formatTime(game.time)}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{game.visitor}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{game.home}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-300">
                  {game.visitor_goals !== null && game.home_goals !== null
                    ? `${game.visitor_goals} - ${game.home_goals}`
                    : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold mb-6 text-white">NHL Dashboard</h1>
      
      <h2 className="text-2xl font-semibold mb-4 text-gray-200">Today's Games</h2>
      {renderContent()}
    </div>
  );
}
