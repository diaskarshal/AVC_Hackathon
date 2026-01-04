import React, { useEffect, useState, useCallback } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import Select from "../components/Select";
import {
  analyticsAPI,
  projectsAPI,
  Project,
  TeamPerformance,
} from "../services/API";

const TeamPerformancePage: React.FC = () => {
  const [performance, setPerformance] = useState<TeamPerformance[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

    const fetchPerformance = useCallback(async () => {
    try {
      setLoading(true);
      const projectId = selectedProject ? parseInt(selectedProject) : undefined;
      const response = await analyticsAPI.getTeamPerformance(projectId);
      setPerformance(response.data.performance);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch team performance");
    } finally {
      setLoading(false);
    }
  }, [selectedProject]);

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    fetchPerformance();
  }, [fetchPerformance]);

  const getPerformanceColor = (rate: number) => {
    if (rate >= 80) return "text-green-600";
    if (rate >= 60) return "text-yellow-600";
    return "text-red-600";
  };

  const getPerformanceBadge = (rate: number) => {
    if (rate >= 80) return { label: "Excellent", color: "bg-green-100 text-green-800" };
    if (rate >= 60) return { label: "Good", color: "bg-yellow-100 text-yellow-800" };
    if (rate >= 40) return { label: "Fair", color: "bg-orange-100 text-orange-800" };
    return { label: "Needs Improvement", color: "bg-red-100 text-red-800" };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading team performance...</div>
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

  const totalTasks = performance.reduce((sum, p) => sum + p.total_tasks, 0);
  const totalCompleted = performance.reduce(
    (sum, p) => sum + p.completed_tasks,
    0
  );
  const avgCompletion =
    performance.length > 0
      ? performance.reduce((sum, p) => sum + p.completion_rate, 0) /
        performance.length
      : 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Team Performance
          </h1>
          <p className="text-gray-600 mt-1">
            Track team member productivity and task completion
          </p>
        </div>
        <button
          onClick={fetchPerformance}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
        >
          Refresh
        </button>
      </div>

      {/* Filter */}
      <Card>
        <CardBody>
          <Select
            label="Filter by Project"
            name="selectedProject"
            value={selectedProject}
            onChange={(e) => setSelectedProject(e.target.value)}
            options={[
              { value: "", label: "All Projects" },
              ...projects.map((p) => ({
                value: p.id.toString(),
                label: p.name,
              })),
            ]}
          />
        </CardBody>
      </Card>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Team Members</div>
            <div className="text-2xl font-bold text-gray-900">
              {performance.length}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Tasks</div>
            <div className="text-2xl font-bold text-gray-900">{totalTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Completed</div>
            <div className="text-2xl font-bold text-green-600">
              {totalCompleted}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Avg. Completion Rate</div>
            <div className={`text-2xl font-bold ${getPerformanceColor(avgCompletion)}`}>
              {avgCompletion.toFixed(1)}%
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Performance Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Worker</TableHead>
            <TableHead>Total Tasks</TableHead>
            <TableHead>Completed</TableHead>
            <TableHead>Avg. Progress</TableHead>
            <TableHead>Completion Rate</TableHead>
            <TableHead>Performance</TableHead>
          </TableHeader>
          <TableBody>
            {performance.length > 0 ? (
              performance.map((member) => {
                const badge = getPerformanceBadge(member.completion_rate);
                return (
                  <tr key={member.worker_name}>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-bold mr-3">
                          {member.worker_name.charAt(0)}
                        </div>
                        <div className="font-medium text-gray-900">
                          {member.worker_name}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="font-semibold">{member.total_tasks}</span>
                    </TableCell>
                    <TableCell>
                      <span className="font-semibold text-green-600">
                        {member.completed_tasks}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${member.avg_progress}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-semibold">
                          {member.avg_progress.toFixed(0)}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center">
                        <div className="w-24 bg-gray-200 rounded-full h-2 mr-2">
                          <div
                            className={`h-2 rounded-full ${
                              member.completion_rate >= 80
                                ? "bg-green-500"
                                : member.completion_rate >= 60
                                ? "bg-yellow-500"
                                : "bg-red-500"
                            }`}
                            style={{ width: `${member.completion_rate}%` }}
                          ></div>
                        </div>
                        <span
                          className={`text-sm font-semibold ${getPerformanceColor(member.completion_rate)}`}
                        >
                          {member.completion_rate.toFixed(0)}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span
                        className={`px-2 py-1 text-xs font-semibold rounded-full ${badge.color}`}
                      >
                        {badge.label}
                      </span>
                    </TableCell>
                  </tr>
                );
              })
            ) : (
              <tr>
                <TableCell colSpan={6}>
                  <div className="text-center py-8 text-gray-500">
                    No performance data available
                  </div>
                </TableCell>
              </tr>
            )}
          </TableBody>
        </Table>
      </Card>

      {/* Performance Insights */}
      {performance.length > 0 && (
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Top Performers
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .sort((a, b) => b.completion_rate - a.completion_rate)
                  .slice(0, 3)
                  .map((member, index) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center">
                        <span className="text-2xl mr-2">
                          {index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉"}
                        </span>
                        <span className="text-sm font-medium">
                          {member.worker_name}
                        </span>
                      </div>
                      <span className="text-sm font-semibold text-green-600">
                        {member.completion_rate.toFixed(0)}%
                      </span>
                    </div>
                  ))}
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Most Active
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .sort((a, b) => b.total_tasks - a.total_tasks)
                  .slice(0, 3)
                  .map((member) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <span className="text-sm font-medium">
                        {member.worker_name}
                      </span>
                      <span className="text-sm font-semibold text-blue-600">
                        {member.total_tasks} tasks
                      </span>
                    </div>
                  ))}
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Needs Support
              </h3>
            </CardHeader>
            <CardBody>
              <div className="space-y-3">
                {[...performance]
                  .filter((p) => p.completion_rate < 60)
                  .sort((a, b) => a.completion_rate - b.completion_rate)
                  .slice(0, 3)
                  .map((member) => (
                    <div
                      key={member.worker_name}
                      className="flex items-center justify-between"
                    >
                      <span className="text-sm font-medium">
                        {member.worker_name}
                      </span>
                      <span className="text-sm font-semibold text-red-600">
                        {member.completion_rate.toFixed(0)}%
                      </span>
                    </div>
                  ))}
                {performance.filter((p) => p.completion_rate < 60).length ===
                  0 && (
                  <div className="text-center text-sm text-gray-500">
                    All team members performing well! 🎉
                  </div>
                )}
              </div>
            </CardBody>
          </Card>
        </div>
      )}
    </div>
  );
};

export default TeamPerformancePage;