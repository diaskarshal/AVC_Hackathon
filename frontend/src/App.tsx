import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import "./App.css";

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route
            path="/tasks"
            element={
              <div className="text-center py-12">
                Tasks page - Coming soon
              </div>
            }
          />
          <Route
            path="/resources"
            element={
              <div className="text-center py-12">
                Resources page - Coming soon
              </div>
            }
          />
          <Route
            path="/budgets"
            element={
              <div className="text-center py-12">
                Budgets page - Coming soon
              </div>
            }
          />
          <Route
            path="/import"
            element={
              <div className="text-center py-12">
                Import page - Coming soon
              </div>
            }
          />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;