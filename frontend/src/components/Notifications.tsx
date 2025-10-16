import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { tasksAPI, Task } from "../services/API";

const Notifications: React.FC = () => {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [overdueTasks, setOverdueTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && user) {
      fetchNotifications();
    }
  }, [isOpen, user]);

  const fetchNotifications = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const response = await tasksAPI.getAll({});
      const tasks = response.data;

      // Filter overdue tasks based on role
      let filtered = tasks.filter((task) => task.is_overdue);

      if (user.role === "worker") {
        filtered = filtered.filter(
          (task) => task.assigned_to === user.worker_name
        );
      } else if (user.role === "manager") {
        const managedProjects = user.managed_projects || [];
        filtered = filtered.filter((task) =>
          managedProjects.includes(task.project_id)
        );
      }

      setOverdueTasks(filtered);
    } catch (err) {
      console.error("Failed to fetch notifications:", err);
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  const notificationCount = overdueTasks.length;

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-white hover:bg-primary-700 rounded-md focus:outline-none"
      >
        <svg
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
        {notificationCount > 0 && (
          <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
            {notificationCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg py-1 z-20 max-h-96 overflow-y-auto">
            <div className="px-4 py-2 border-b border-gray-200">
              <div className="text-sm font-semibold text-gray-900">
                Notifications
              </div>
            </div>

            {loading ? (
              <div className="px-4 py-8 text-center text-gray-500">
                Loading...
              </div>
            ) : overdueTasks.length > 0 ? (
              <div className="divide-y divide-gray-200">
                {overdueTasks.slice(0, 5).map((task) => (
                  <div key={task.id} className="px-4 py-3 hover:bg-gray-50">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <svg
                          className="h-5 w-5 text-red-600"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fillRule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                            clipRule="evenodd"
                          />
                        </svg>
                      </div>
                      <div className="ml-3 flex-1">
                        <p className="text-sm font-medium text-gray-900">
                          {task.name}
                        </p>
                        <p className="text-xs text-red-600 mt-1">
                          Overdue since{" "}
                          {task.planned_end_date
                            ? new Date(
                                task.planned_end_date
                              ).toLocaleDateString()
                            : "N/A"}
                        </p>
                        {task.assigned_to && (
                          <p className="text-xs text-gray-500 mt-1">
                            Assigned to: {task.assigned_to}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {overdueTasks.length > 5 && (
                  <div className="px-4 py-2 text-center text-sm text-primary-600 hover:bg-gray-50">
                    +{overdueTasks.length - 5} more overdue tasks
                  </div>
                )}
              </div>
            ) : (
              <div className="px-4 py-8 text-center text-gray-500">
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
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <p className="mt-2 text-sm">No overdue tasks!</p>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Notifications;