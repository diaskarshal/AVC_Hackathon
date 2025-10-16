import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import PrivateRoute from "./components/PrivateRoute";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Tasks from "./pages/Tasks";
import Resources from "./pages/Resources";
import Budgets from "./pages/Budgets";
import Import from "./pages/Import";

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<Login />} />

          {/* Admin Routes */}
          <Route
            path="/admin/dashboard"
            element={
              <PrivateRoute allowedRoles={["admin"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Manager Routes */}
          <Route
            path="/manager/dashboard"
            element={
              <PrivateRoute allowedRoles={["manager"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Worker Routes */}
          <Route
            path="/worker/dashboard"
            element={
              <PrivateRoute allowedRoles={["worker"]}>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/worker/my-tasks"
            element={
              <PrivateRoute allowedRoles={["worker"]}>
                <Layout>
                  <Tasks />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Shared Routes (with role-based access) */}
          <Route
            path="/projects"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Projects />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/tasks"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Tasks />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/resources"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Resources />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/budgets"
            element={
              <PrivateRoute allowedRoles={["admin", "manager"]}>
                <Layout>
                  <Budgets />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/import"
            element={
              <PrivateRoute allowedRoles={["admin"]}>
                <Layout>
                  <Import />
                </Layout>
              </PrivateRoute>
            }
          />

          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;