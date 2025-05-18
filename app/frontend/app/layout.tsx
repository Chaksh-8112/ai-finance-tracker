// File: app/frontend/app/components/StatCard.tsx
use "client";
import React from "react";
import { TrendingUp, TrendingDown, LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  delta: string;
  deltaPositive: boolean;
  Icon: LucideIcon;
}

export default function StatCard({
  title,
  value,
  delta,
  deltaPositive,
  Icon,
}: StatCardProps) {
  return (
    <div className="bg-white dark:bg-gray-900 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-800">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
          <p
            className={`text-sm flex items-center ${
              deltaPositive
                ? "text-green-600 dark:text-green-400"
                : "text-red-600 dark:text-red-400"
            }`}
          >
            {deltaPositive ? <TrendingUp size={16} className="mr-1" /> : <TrendingDown size={16} className="mr-1" />}
            {delta}
          </p>
        </div>
        <div
          className={`p-2 rounded-full ${
            deltaPositive ? "bg-green-100 dark:bg-green-900/30" : "bg-red-100 dark:bg-red-900/30"
          }`}
        >
          <Icon size={20} className={deltaPositive ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"} />
        </div>
      </div>
    </div>
  );
}

// File: app/frontend/app/layout.tsx
"use client";
import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import StatCard from "./components/StatCard";
import { TrendingUp, TrendingDown, BarChart2, Activity, DollarSign } from "lucide-react";

// Sample financial data
const stockData = [
  { name: 'Jan', value: 4000 },
  { name: 'Feb', value: 3000 },
  { name: 'Mar', value: 5000 },
  { name: 'Apr', value: 2780 },
  { name: 'May', value: 1890 },
  { name: 'Jun', value: 2390 },
  { name: 'Jul', value: 3490 },
  { name: 'Aug', value: 4000 },
  { name: 'Sep', value: 5200 },
  { name: 'Oct', value: 5600 },
  { name: 'Nov', value: 4900 },
  { name: 'Dec', value: 6100 },
];

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  
  return (
    <div className="space-y-6">
      {/* Dashboard header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Financial Dashboard</h1>
        <div className="flex space-x-2">
          <select className="bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 border border-gray-300 dark:border-gray-700 rounded-md px-3 py-1">
            <option>Last 30 Days</option>
            <option>Last Quarter</option>
            <option>Year to Date</option>
            <option>Last Year</option>
          </select>
          <button className="bg-red-600 text-white px-3 py-1 rounded-md hover:bg-red-700">Export</button>
        </div>
      </div>
      
      {/* Stats overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          title="Total Assets"
          value="$124,765.87"
          delta="+2.45%"
          deltaPositive={true}
          Icon={TrendingUp}
        />
        
        <StatCard
          title="Liabilities"
          value="$38,275.00"
          delta="+0.8%"
          deltaPositive={false}
          Icon={BarChart2}
        />
        
        <StatCard
          title="Monthly Income"
          value="$7,842.32"
          delta="+4.6%"
          deltaPositive={true}
          Icon={Activity}
        />
        
        <StatCard
          title="Net Worth"
          value="$86,490.87"
          delta="+3.2%"
          deltaPositive={true}
          Icon={DollarSign}
        />
      </div>
      
      {/* Chart section */}
      <div className="bg-white dark:bg-gray-900 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-800">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Portfolio Performance</h2>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={stockData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: 'none', color: '#F9FAFB' }} />
              <Line type="monotone" dataKey="value" stroke="#EF4444" strokeWidth={2} dot={{ stroke: '#EF4444', strokeWidth: 2, r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Recent transactions */}
      <div className="bg-white dark:bg-gray-900 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-800">
        <h2 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Recent Transactions</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-left bg-gray-50 dark:bg-gray-800">
                <th className="p-3 text-sm font-medium text-gray-700 dark:text-gray-300">Date</th>
                <th className="p-3 text-sm font-medium text-gray-700 dark:text-gray-300">Description</th>
                <th className="p-3 text-sm font-medium text-gray-700 dark:text-gray-300">Category</th>
                <th className="p-3 text-sm font-medium text-gray-700 dark:text-gray-300">Amount</th>
                <th className="p-3 text-sm font-medium text-gray-700 dark:text-gray-300">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">May 16, 2025</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Amazon Purchase</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Shopping</td>
                <td className="p-3 text-sm text-red-600 dark:text-red-400">-$84.29</td>
                <td className="p-3"><span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300">Completed</span></td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">May 15, 2025</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Salary Deposit</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Income</td>
                <td className="p-3 text-sm text-green-600 dark:text-green-400">+$3,250.00</td>
                <td className="p-3"><span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300">Completed</span></td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">May 14, 2025</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Mortgage Payment</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Housing</td>
                <td className="p-3 text-sm text-red-600 dark:text-red-400">-$1,450.00</td>
                <td className="p-3"><span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300">Completed</span></td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">May 12, 2025</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Stock Dividend</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Investment</td>
                <td className="p-3 text-sm text-green-600 dark:text-green-400">+$327.50</td>
                <td className="p-3"><span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300">Completed</span></td>
              </tr>
              <tr className="hover:bg-gray-50 dark:hover:bg-gray-800">
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">May 10, 2025</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Grocery Shopping</td>
                <td className="p-3 text-sm text-gray-700 dark:text-gray-300">Food</td>
                <td className="p-3 text-sm text-red-600 dark:text-red-400">-$98.76</td>
                <td className="p-3"><span className="px-2 py-1 text-xs rounded-full bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300">Completed</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"use client";

import "./globals.css";
import { useState, useEffect } from "react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<"light" | "dark">("dark");

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  return (
    <html lang="en" className={theme}>
      <body className="bg-white dark:bg-surface text-black dark:text-on-surface font-sans">
        <header className="p-4 flex justify-between items-center bg-surface-light dark:bg-surface border-b border-gray-200 dark:border-gray-700">
          <nav className="flex space-x-4">
            <a href="/" className="text-primary dark:text-secondary hover:text-accent font-medium">Home</a>
            <a href="/upload" className="text-primary dark:text-secondary hover:text-accent font-medium">Upload</a>
            <a href="/reports" className="text-primary dark:text-secondary hover:text-accent font-medium">Reports</a>
          </nav>
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="bg-primary text-on-surface p-2 rounded hover:bg-primary-light transition-colors"
          >
            {theme === "dark" ? "☀️" : "🧙‍♀️"}
          </button>
        </header>
        <main className="p-4">
          {children}
        </main>
      </body>
    </html>
  );
}