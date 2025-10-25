'use client'; // This component will use client-side hooks like usePathname

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
// To use heroicons, you'll need to install them: npm install @heroicons/react
import { 
  HomeIcon, 
  CalendarIcon, 
  TableCellsIcon, 
  UserIcon, 
  UserGroupIcon, 
  ChartBarIcon 
} from '@heroicons/react/24/outline'; 

// Define the navigation links
const navigation = [
  { name: 'Dashboard', href: '/nhl', icon: HomeIcon },
  { name: 'Full Schedule', href: '/nhl/schedule', icon: TableCellsIcon },
  { name: 'Calendar', href: '/nhl/calendar', icon: CalendarIcon },
];

// Placeholder links for future features
const futureFeatures = [
  { name: 'Player Info', icon: UserIcon },
  { name: 'Team Info', icon: UserGroupIcon },
  { name: 'Predictions', icon: ChartBarIcon },
];

// Helper function to dynamically apply classes
function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex w-64 flex-col bg-gray-800 border-r border-gray-700">
      <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
        <div className="flex flex-shrink-0 items-center px-4">
          <h2 className="text-2xl font-bold text-white">NHL Section</h2>
        </div>
        <nav className="mt-5 flex-1" aria-label="Sidebar">
          <div className="space-y-1 px-2">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={classNames(
                  pathname === item.href
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white',
                  'group flex items-center rounded-md px-2 py-2 text-sm font-medium transition-colors'
                )}
              >
                <item.icon
                  className="mr-3 h-6 w-6 flex-shrink-0 text-gray-400 group-hover:text-gray-300"
                  aria-hidden="true"
                />
                {item.name}
              </Link>
            ))}
          </div>
          <div className="mt-6 pt-6">
            <div className="space-y-1 px-2">
              <h3 className="px-2 text-xs font-semibold uppercase text-gray-400">
                Future Features
              </h3>
              {futureFeatures.map((item) => (
                <div
                  key={item.name}
                  className="group flex items-center rounded-md px-2 py-2 text-sm font-medium text-gray-500 cursor-not-allowed"
                >
                  <item.icon
                    className="mr-3 h-6 w-6 flex-shrink-0"
                    aria-hidden="true"
                  />
                  {item.name}
                </div>
              ))}
            </div>
          </div>
        </nav>
      </div>
    </div>
  );
}
