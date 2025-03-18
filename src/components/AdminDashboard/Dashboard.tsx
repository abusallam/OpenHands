import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext'; // Assuming you have an auth context
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import { UserStats, ProjectStats, AIStats } from '../types'; // You'll need to define these types

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    users: null,
    projects: null,
    aiMetrics: null,
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [users, projects, aiMetrics] = await Promise.all([
          axios.get('/api/admin/users/stats'),
          axios.get('/api/admin/projects/stats'),
          axios.get('/api/admin/ai/metrics'),
        ]);
        
        setStats({
          users: users.data,
          projects: projects.data,
          aiMetrics: aiMetrics.data,
        });
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Sidebar Navigation */}
      <aside className="fixed left-0 top-0 h-screen w-64 bg-gray-800 p-4">
        <div className="mb-8">
          <h1 className="text-xl font-bold">AI Coder Admin</h1>
          <p className="text-sm text-gray-400">Welcome, {user?.name}</p>
        </div>
        
        <nav>
          <ul className="space-y-2">
            <li>
              <a href="/admin/dashboard" className="nav-link">
                Dashboard
              </a>
            </li>
            <li>
              <a href="/admin/users" className="nav-link">
                User Management
              </a>
            </li>
            <li>
              <a href="/admin/projects" className="nav-link">
                Projects
              </a>
            </li>
            <li>
              <a href="/admin/ai-metrics" className="nav-link">
                AI Metrics
              </a>
            </li>
            <li>
              <a href="/admin/database" className="nav-link">
                Database Status
              </a>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="ml-64 p-8">
        {/* Database Status */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Database Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-gray-400">Connection Status</h3>
              <p className="text-2xl font-bold text-green-500">Connected</p>
              <p className="text-sm text-gray-400">Host: {process.env.DATABASE_HOST}</p>
              <p className="text-sm text-gray-400">Database: {process.env.DATABASE_NAME}</p>
            </div>
          </div>
        </div>

        {/* User Statistics */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">User Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {stats.users && (
              <>
                <div className="stat-card">
                  <h3>Total Users</h3>
                  <p className="text-2xl">{stats.users.total}</p>
                </div>
                <div className="stat-card">
                  <h3>Active Users</h3>
                  <p className="text-2xl">{stats.users.active}</p>
                </div>
                <div className="stat-card">
                  <h3>New Users (Today)</h3>
                  <p className="text-2xl">{stats.users.newToday}</p>
                </div>
              </>
            )}
          </div>
        </div>

        {/* AI Metrics */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">AI Performance Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {stats.aiMetrics && (
              <>
                <div className="bg-gray-800 p-6 rounded-lg">
                  <h3>Response Times</h3>
                  <Line 
                    data={stats.aiMetrics.responseTimeData}
                    options={{
                      responsive: true,
                      scales: {
                        y: { grid: { color: '#374151' } },
                        x: { grid: { color: '#374151' } }
                      }
                    }}
                  />
                </div>
                <div className="bg-gray-800 p-6 rounded-lg">
                  <h3>Success Rate</h3>
                  <Bar 
                    data={stats.aiMetrics.successRateData}
                    options={{
                      responsive: true,
                      scales: {
                        y: { grid: { color: '#374151' } },
                        x: { grid: { color: '#374151' } }
                      }
                    }}
                  />
                </div>
              </>
            )}
          </div>
        </div>

        {/* Recent Activity Table */}
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          <h2 className="text-2xl font-bold p-6">Recent Activity</h2>
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left">Timestamp</th>
                <th className="px-6 py-3 text-left">User</th>
                <th className="px-6 py-3 text-left">Action</th>
                <th className="px-6 py-3 text-left">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {stats.projects?.recentActivity?.map((activity) => (
                <tr key={activity.id}>
                  <td className="px-6 py-4">{new Date(activity.timestamp).toLocaleString()}</td>
                  <td className="px-6 py-4">{activity.user}</td>
                  <td className="px-6 py-4">{activity.action}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded ${
                      activity.status === 'success' ? 'bg-green-500' : 'bg-red-500'
                    }`}>
                      {activity.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard; 