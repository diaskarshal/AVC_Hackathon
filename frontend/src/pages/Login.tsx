import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { authAPI } from "../services/API";
import { DemoUser } from "../types/auth";
import Button from "../components/Button";
import Input from "../components/Input";

const Login: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>([]);
  const { login } = useAuth();

  useEffect(() => {
    fetchDemoUsers();
  }, []);

  const fetchDemoUsers = async () => {
    try {
      const response = await authAPI.getDemoUsers();
      setDemoUsers(response.data);
    } catch (err) {
      console.error("Failed to fetch demo users:", err);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login({ username, password });
    } catch (err: any) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = (user: DemoUser) => {
    setUsername(user.username);
    // Extract password from hint (e.g., "Password: admin123")
    const passwordMatch = user.hint.match(/Password: (\w+)/);
    if (passwordMatch) {
      setPassword(passwordMatch[1]);
    }
  };

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
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center px-4">
      <div className="max-w-6xl w-full grid md:grid-cols-2 gap-8">
        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              BuildFlow ERP
            </h1>
            <p className="text-gray-600">
              Construction Project Management System
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Username"
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />

            {error && (
              <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={loading}
            >
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Demo accounts available →</p>
          </div>
        </div>

        {/* Demo Users Panel */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Demo Accounts
          </h2>
          <p className="text-gray-600 mb-6">
            Click any account to quick-fill the login form
          </p>

          <div className="space-y-3">
            {demoUsers.map((user) => (
              <button
                key={user.username}
                onClick={() => quickLogin(user)}
                className="w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-gray-900">
                    {user.name}
                  </span>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleBadgeColor(user.role)}`}
                  >
                    {user.role}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <div>Username: {user.username}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    {user.hint}
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">
              Role Descriptions:
            </h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>
                <strong>Admin:</strong> Full system access
              </li>
              <li>
                <strong>Manager:</strong> Manage assigned projects
              </li>
              <li>
                <strong>Worker:</strong> View and update own tasks
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;