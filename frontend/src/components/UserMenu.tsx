import React, { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { Link } from "react-router-dom";

const UserMenu: React.FC = () => {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) return null;

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case "admin":
        return "bg-red-100 text-red-800";
      case "manager":
        return "bg-blue-100 text-blue-800";
      case "worker":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-3 focus:outline-none"
      >
        <div className="text-right">
          <div className="text-sm font-medium text-white">{user.name}</div>
          <div
            className={`text-xs px-2 py-0.5 rounded-full inline-block ${getRoleBadgeColor(user.role)}`}
          >
            {user.role}
          </div>
        </div>
        <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-primary-600 font-bold">
          {user.name.charAt(0)}
        </div>
      </button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          ></div>
          <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20">
            <div className="px-4 py-2 border-b border-gray-200">
              <div className="text-sm font-medium text-gray-900">
                {user.name}
              </div>
              <div className="text-xs text-gray-500">{user.email}</div>
            </div>
            
            {/* ADD PROFILE LINK */}
            <Link
              to="/profile"
              onClick={() => setIsOpen(false)}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              My Profile
            </Link>
            
            <button
              onClick={logout}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default UserMenu;