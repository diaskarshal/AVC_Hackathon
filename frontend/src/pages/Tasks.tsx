import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import { Table, TableHeader, TableBody, TableHead, TableCell } from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import { exportToCSV } from '../utils/export';
import { tasksAPI, projectsAPI, Task, Project } from "../services/API";

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");
  const [filterStatus, setFilterStatus] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    name: "",
    description: "",
    status: "not_started",
    priority: "medium",
    start_date: "",
    planned_end_date: "",
    progress_percentage: 0,
    assigned_to: "",
  });

  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await tasksAPI.getAll();
      setTasks(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.getAll();
      setProjects(response.data);
    } catch (err) {
      console.error("Failed to fetch projects:", err);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const submitData: any = {
        project_id: parseInt(formData.project_id),
        name: formData.name,
        description: formData.description || undefined,
        status: formData.status,
        priority: formData.priority,
        progress_percentage: parseFloat(formData.progress_percentage.toString()),
        assigned_to: formData.assigned_to || undefined,
      };

      // Only include dates if they are filled
      if (formData.start_date) {
        submitData.start_date = new Date(formData.start_date).toISOString();
      }
      if (formData.planned_end_date) {
        submitData.planned_end_date = new Date(formData.planned_end_date).toISOString();
      }

      if (editingTask) {
        await tasksAPI.update(editingTask.id, submitData);
      } else {
        await tasksAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchTasks();
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? JSON.stringify(err.response.data.detail)
        : err.message || "Failed to save task";
      alert(errorMsg);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this task?")) {
      try {
        await tasksAPI.delete(id);
        fetchTasks();
      } catch (err: any) {
        alert(err.message || "Failed to delete task");
      }
    }
  };

  const handleExport = () => {
    const exportData = filteredTasks.map((task) => ({
      ID: task.id,
      "Project ID": task.project_id,
      Name: task.name,
      Status: task.status,
      Priority: task.priority,
      "Assigned To": task.assigned_to || "Unassigned",
      "Start Date": task.start_date
        ? new Date(task.start_date).toLocaleDateString()
        : "N/A",
      "End Date": task.planned_end_date
        ? new Date(task.planned_end_date).toLocaleDateString()
        : "N/A",
      "Progress %": task.progress_percentage,
      Overdue: task.is_overdue ? "Yes" : "No",
    }));

    exportToCSV(exportData, "tasks");
  };

  const openEditModal = (task: Task) => {
    setEditingTask(task);
    setFormData({
      project_id: task.project_id.toString(),
      name: task.name,
      description: task.description || "",
      status: task.status,
      priority: task.priority,
      start_date: task.start_date?.split("T")[0] || "",
      planned_end_date: task.planned_end_date?.split("T")[0] || "",
      progress_percentage: task.progress_percentage,
      assigned_to: task.assigned_to || "",
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      name: "",
      description: "",
      status: "not_started",
      priority: "medium",
      start_date: "",
      planned_end_date: "",
      progress_percentage: 0,
      assigned_to: "",
    });
    setEditingTask(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      not_started: "bg-gray-100 text-gray-800",
      in_progress: "bg-blue-100 text-blue-800",
      completed: "bg-green-100 text-green-800",
      delayed: "bg-yellow-100 text-yellow-800",
      blocked: "bg-red-100 text-red-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      low: "text-gray-600",
      medium: "text-blue-600",
      high: "text-orange-600",
      critical: "text-red-600",
    };
    return colors[priority] || "text-gray-600";
  };

  const filteredTasks = tasks.filter((task) => {
    if (filterProject && task.project_id.toString() !== filterProject) return false;
    if (filterStatus && task.status !== filterStatus) return false;
    return true;
  });

  const totalTasks = filteredTasks.length;
  const completedTasks = filteredTasks.filter(t => t.status === "completed").length;
  const inProgressTasks = filteredTasks.filter(t => t.status === "in_progress").length;
  const overdueTasks = filteredTasks.filter(t => t.is_overdue).length;
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks * 100) : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading tasks...</div>
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

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tasks</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>Add New Task</Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Tasks</div>
            <div className="text-2xl font-bold text-gray-900">{totalTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Completed</div>
            <div className="text-2xl font-bold text-green-600">{completedTasks}</div>
            <div className="text-xs text-gray-500 mt-1">
              {completionRate.toFixed(1)}% completion rate
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">In Progress</div>
            <div className="text-2xl font-bold text-blue-600">{inProgressTasks}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Overdue</div>
            <div className="text-2xl font-bold text-red-600">{overdueTasks}</div>
          </CardBody>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select
              label="Filter by Project"
              name="filterProject"
              value={filterProject}
              onChange={(e) => setFilterProject(e.target.value)}
              options={[
                { value: "", label: "All Projects" },
                ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
              ]}
            />
            <Select
              label="Filter by Status"
              name="filterStatus"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              options={[
                { value: "", label: "All Statuses" },
                { value: "not_started", label: "Not Started" },
                { value: "in_progress", label: "In Progress" },
                { value: "completed", label: "Completed" },
                { value: "delayed", label: "Delayed" },
                { value: "blocked", label: "Blocked" },
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => {
                  setFilterProject("");
                  setFilterStatus("");
                }}
                className="w-full"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Tasks Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Task Name</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Priority</TableHead>
            <TableHead>Progress</TableHead>
            <TableHead>Assigned To</TableHead>
            <TableHead>Due Date</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredTasks.map((task) => (
              <tr key={task.id}>
                <TableCell>
                  <div className="font-medium text-gray-900">{task.name}</div>
                  {task.description && (
                    <div className="text-gray-500 text-xs mt-1 truncate max-w-xs">
                      {task.description}
                    </div>
                  )}
                </TableCell>
                <TableCell>
                  <div className="text-gray-900">
                    {projects.find((p) => p.id === task.project_id)?.name || `Project #${task.project_id}`}
                  </div>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}
                  >
                    {task.status.replace("_", " ")}
                  </span>
                </TableCell>
                <TableCell>
                  <span className={`font-semibold capitalize ${getPriorityColor(task.priority)}`}>
                    {task.priority}
                  </span>
                </TableCell>
                <TableCell>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${task.progress_percentage}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    {task.progress_percentage}%
                  </div>
                </TableCell>
                <TableCell>
                  {task.assigned_to || <span className="text-gray-400">Unassigned</span>}
                </TableCell>
                <TableCell>
                  {task.planned_end_date ? (
                    <div>
                      <div className="text-gray-900">
                        {new Date(task.planned_end_date).toLocaleDateString()}
                      </div>
                      {task.is_overdue && (
                        <span className="text-xs text-red-600 font-semibold">Overdue</span>
                      )}
                    </div>
                  ) : (
                    <span className="text-gray-400">No date</span>
                  )}
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(task)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </div>
                </TableCell>
              </tr>
            ))}
          </TableBody>
        </Table>
        {filteredTasks.length === 0 && (
          <div className="text-center py-12 text-gray-500">No tasks found</div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingTask ? "Edit Task" : "Create New Task"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleInputChange}
            options={[
              { value: "", label: "Select a project" },
              ...projects.map((p) => ({ value: p.id.toString(), label: p.name })),
            ]}
            required
          />

          <Input
            label="Task Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <TextArea
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            rows={3}
          />

          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleInputChange}
              options={[
                { value: "not_started", label: "Not Started" },
                { value: "in_progress", label: "In Progress" },
                { value: "completed", label: "Completed" },
                { value: "delayed", label: "Delayed" },
                { value: "blocked", label: "Blocked" },
              ]}
              required
            />

            <Select
              label="Priority"
              name="priority"
              value={formData.priority}
              onChange={handleInputChange}
              options={[
                { value: "low", label: "Low" },
                { value: "medium", label: "Medium" },
                { value: "high", label: "High" },
                { value: "critical", label: "Critical" },
              ]}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Start Date"
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
            />

            <Input
              label="Planned End Date"
              type="date"
              name="planned_end_date"
              value={formData.planned_end_date}
              onChange={handleInputChange}
            />
          </div>

          <Input
            label="Progress (%)"
            type="number"
            name="progress_percentage"
            value={formData.progress_percentage}
            onChange={handleInputChange}
            placeholder="0-100"
          />

          <Input
            label="Assigned To"
            name="assigned_to"
            value={formData.assigned_to}
            onChange={handleInputChange}
            placeholder="Team member name"
          />

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsModalOpen(false);
                resetForm();
              }}
            >
              Cancel
            </Button>
            <Button type="submit">
              {editingTask ? "Update Task" : "Create Task"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Tasks;