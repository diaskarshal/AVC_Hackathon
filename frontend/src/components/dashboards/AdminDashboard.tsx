import React from "react";
import { Card, CardHeader, CardBody } from "../Card";
import { DashboardStats } from "../../services/API";
import ChartsSection from "./ChartsSection";

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
      {/* AVC GROUP company banner */}
      <div className="rounded-xl bg-gradient-to-r from-primary-700 to-primary-500 px-6 py-5 text-white shadow-lg">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-white">
                <span className="text-primary-700 font-black text-sm">AVC</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold leading-none">AVC GROUP</h1>
                <p className="text-primary-200 text-xs font-medium tracking-widest uppercase mt-0.5">BuildFlow — система управления ремонтами</p>
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-black">1 000+</p>
              <p className="text-primary-200 text-xs leading-tight">сотрудников<br />в штате</p>
            </div>
            <div className="border-l border-primary-400 pl-4">
              <p className="text-2xl font-black">150+</p>
              <p className="text-primary-200 text-xs leading-tight">квалиф.<br />ИТР</p>
            </div>
            <div className="border-l border-primary-400 pl-4">
              <p className="text-2xl font-black">47+</p>
              <p className="text-primary-200 text-xs leading-tight">установок<br />АНПЗ · ПНХЗ</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Admin Dashboard
        </h1>
        <p className="text-gray-600 mt-1">
          Complete overview of all projects and resources
        </p>
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

      {/* Plotly KPI Charts */}
      <ChartsSection />

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