import React from "react";
import { Link, useLocation } from "react-router-dom";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path
      ? "bg-primary-700 text-white"
      : "text-gray-300 hover:bg-primary-700 hover:text-white";
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-primary-600 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Link
                to="/"
                className="flex-shrink-0 text-white text-xl font-bold"
              >
                BuildFlow
              </Link>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <Link
                    to="/"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/")}`}
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/projects"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/projects")}`}
                  >
                    Projects
                  </Link>
                  <Link
                    to="/tasks"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/tasks")}`}
                  >
                    Tasks
                  </Link>
                  <Link
                    to="/resources"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/resources")}`}
                  >
                    Resources
                  </Link>
                  <Link
                    to="/budgets"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/budgets")}`}
                  >
                    Budgets
                  </Link>
                  <Link
                    to="/import"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive("/import")}`}
                  >
                    Import Data
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;