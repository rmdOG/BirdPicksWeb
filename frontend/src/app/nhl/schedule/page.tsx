'use client'; 

import React, { useState, useEffect } from 'react';

// Define a TypeScript type for a single schedule item.
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

// This is the component for the full schedule list page.
export default function FullSchedulePage() {
  const [schedule, setSchedule] = useState<ScheduleItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await fetch('http://localhost:8000/schedule/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: ScheduleItem[] = await response.json();
        setSchedule(data); 
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

  // Helper function to format the time nicely
  const formatTime = (timeString: string) => {
    if (!timeString) return 'TBD';
    const parts = timeString.split(':');
    if (parts.length < 2) return 'Invalid Time';

    const [hours, minutes] = parts;
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes));
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
  };
  
  if (isLoading) {
    return (
      <div className="flex w-full flex-col items-center justify-center p-24">
        <h1 className="text-4xl font-bold">Loading Full Schedule...</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex w-full flex-col items-center justify-center p-24 text-red-400">
        <h1 className="text-4xl font-bold">Error</h1>
        <p className="mt-4 text-lg">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold mb-6 text-center text-white">Full NHL Schedule 25-26</h1>
      
      <div className="overflow-x-auto rounded-lg border border-gray-700">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-800">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Date</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-segment_extraction_train_cal_march_2018 text-gray-300 uppercase tracking-wider">Time</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Away Team</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Home Team</th>
              <th scope="col" className="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Score</th>
            </tr>
          </thead>
          <tbody className="bg-gray-800/50 divide-y divide-gray-700">
            {schedule.map((game) => (
              <tr key={game.id} className="hover:bg-gray-700/50 transition-colors duration-200">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{new Date(game.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' })}</td>
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
    </div>
  );
}
