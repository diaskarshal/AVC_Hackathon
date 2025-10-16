import React from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardBody } from "../Card";
import { DashboardStats } from "../../services/API";

interface AdminDashboardProps {
  stats: DashboardStats;
  onRefresh: () => void;
}

const AdminDashboard: React.FC<AdminDashboardProps> = ({
  stats,
  onRefresh,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Admin Dashboard
          </h1>
          <p className="text-gray-600 mt-1">
            Complete overview of all projects and resources
          </p>
        </div>
        <button
          onClick={onRefresh}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* Total Projects */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-primary-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Projects
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_projects}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.active_projects} active,{" "}
              {stats.completed_projects} completed
            </div>
          </CardBody>
        </Card>

        {/* Budget */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Budget
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    ${(stats.total_budget / 1000000).toFixed(1)}M
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              ${(stats.total_spent / 1000000).toFixed(1)}M spent (
              {stats.budget_utilization.toFixed(1)}%)
            </div>
          </CardBody>
        </Card>

        {/* Tasks */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.completed_tasks} completed (
              {stats.task_completion_rate.toFixed(1)}%)
            </div>
          </CardBody>
        </Card>

        {/* Overdue Tasks */}
        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-red-500 rounded-md p-3">
                <svg
                  className="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Overdue Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.overdue_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              Requires attention
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Quick Actions
          </h3>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <Link
              to="/projects"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              Manage Projects
            </Link>
            <Link
              to="/tasks"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              View All Tasks
            </Link>
            <Link
              to="/import"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              Import Data
            </Link>
            <Link
              to="/users"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
            >
              Manage Users
            </Link>
          </div>
        </CardBody>
      </Card>

      {/* System Health */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Budget Overview
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Budget Utilization</span>
                  <span className="font-semibold">
                    {stats.budget_utilization.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      stats.budget_utilization > 90
                        ? "bg-red-600"
                        : stats.budget_utilization > 75
                        ? "bg-yellow-500"
                        : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(stats.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Total Budget</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_budget / 1000000).toFixed(2)}M
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Spent</p>
                  <p className="text-lg font-semibold">
                    ${(stats.total_spent / 1000000).toFixed(2)}M
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Task Completion
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Completion Rate</span>
                  <span className="font-semibold">
                    {stats.task_completion_rate.toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{
                      width: `${Math.min(stats.task_completion_rate, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 pt-4 border-t">
                <div>
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-lg font-semibold">{stats.total_tasks}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Completed</p>
                  <p className="text-lg font-semibold text-green-600">
                    {stats.completed_tasks}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Overdue</p>
                  <p className="text-lg font-semibold text-red-600">
                    {stats.overdue_tasks}
                  </p>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;