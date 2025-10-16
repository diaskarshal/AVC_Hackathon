import React from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardBody } from "../Card";

interface WorkerStats {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  not_started_tasks: number;
  overdue_tasks: number;
  upcoming_tasks: number;
  task_completion_rate: number;
}

interface WorkerDashboardProps {
  stats: WorkerStats;
  onRefresh: () => void;
}

const WorkerDashboard: React.FC<WorkerDashboardProps> = ({
  stats,
  onRefresh,
}) => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Worker Dashboard
          </h1>
          <p className="text-gray-600 mt-1">Manage your assigned tasks</p>
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
                    My Tasks
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.total_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Total assigned</div>
          </CardBody>
        </Card>

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
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Completed
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.completed_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">
              {stats.task_completion_rate.toFixed(0)}% rate
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
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
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    In Progress
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.in_progress_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Currently working</div>
          </CardBody>
        </Card>

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
                    Overdue
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.overdue_tasks}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="mt-2 text-sm text-gray-500">Need attention</div>
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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Link
              to="/worker/my-tasks"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              View My Tasks
            </Link>
            <Link
              to="/worker/my-tasks?filter=overdue"
              className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              View Overdue Tasks
            </Link>
          </div>
        </CardBody>
      </Card>

      {/* Task Status Overview */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Task Status
            </h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Completed</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-green-500 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.completed_tasks / stats.total_tasks) * 100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.completed_tasks}
                  </span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">In Progress</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-yellow-500 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.in_progress_tasks / stats.total_tasks) *
                              100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.in_progress_tasks}
                  </span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Not Started</span>
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2 mr-2">
                    <div
                      className="bg-gray-400 h-2 rounded-full"
                      style={{
                        width: `${
                          stats.total_tasks > 0
                            ? (stats.not_started_tasks / stats.total_tasks) *
                              100
                            : 0
                        }%`,
                      }}
                    ></div>
                  </div>
                  <span className="text-sm font-semibold">
                    {stats.not_started_tasks}
                  </span>
                </div>
              </div>
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Upcoming Deadlines
            </h3>
          </CardHeader>
          <CardBody>
            <div className="text-center py-8">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Tasks Due Soon
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                You have {stats.upcoming_tasks} task(s) due in the next 7 days
              </p>
              <div className="mt-6">
                <Link
                  to="/worker/my-tasks?filter=upcoming"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  View Upcoming Tasks
                </Link>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  );
};

export default WorkerDashboard;