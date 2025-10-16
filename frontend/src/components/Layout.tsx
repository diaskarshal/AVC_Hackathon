import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import UserMenu from "./UserMenu";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { user } = useAuth();

  const isActive = (path: string) => {
    return location.pathname === path
      ? "bg-primary-700 text-white"
      : "text-gray-300 hover:bg-primary-700 hover:text-white";
  };

  // Different navigation based on role
  const getNavigationLinks = () => {
    if (!user) return [];

    if (user.role === "admin") {
      return [
        { path: "/admin/dashboard", label: "Dashboard" },
        { path: "/projects", label: "Projects" },
        { path: "/tasks", label: "Tasks" },
        { path: "/resources", label: "Resources" },
        { path: "/budgets", label: "Budgets" },
        { path: "/import", label: "Import Data" },
      ];
    } else if (user.role === "manager") {
      return [
        { path: "/manager/dashboard", label: "Dashboard" },
        { path: "/projects", label: "Projects" },
        { path: "/tasks", label: "Tasks" },
        { path: "/resources", label: "Resources" },
        { path: "/budgets", label: "Budgets" },
      ];
    } else {
      // worker
      return [
        { path: "/worker/dashboard", label: "Dashboard" },
        { path: "/worker/my-tasks", label: "My Tasks" },
      ];
    }
  };

  const navLinks = getNavigationLinks();

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
                  {navLinks.map((link) => (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`px-3 py-2 rounded-md text-sm font-medium ${isActive(link.path)}`}
                    >
                      {link.label}
                    </Link>
                  ))}
                </div>
              </div>
            </div>
            <UserMenu />
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