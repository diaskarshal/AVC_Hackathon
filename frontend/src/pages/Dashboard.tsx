import React, { useEffect, useState } from "react";
import { analyticsAPI, DashboardStats, WorkerStats } from "../services/API";
import { useAuth } from "../contexts/AuthContext";
import AdminDashboard from "../components/dashboards/AdminDashboard";
import ManagerDashboard from "../components/dashboards/ManagerDashboard";
import WorkerDashboard from "../components/dashboards/WorkerDashboard";

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | WorkerStats | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await analyticsAPI.getDashboard();
      setStats(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch dashboard data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error: {error}
      </div>
    );
  }

  if (!stats || !user) return null;

  if (user.role === "admin") {
    return (
      <AdminDashboard
        stats={stats as DashboardStats}
        onRefresh={fetchDashboard}
      />
    );
  } else if (user.role === "manager") {
    return (
      <ManagerDashboard
        stats={stats as DashboardStats}
        onRefresh={fetchDashboard}
      />
    );
  } else {
    return (
      <WorkerDashboard
        stats={stats as WorkerStats}
        onRefresh={fetchDashboard}
      />
    );
  }
};

export default Dashboard;