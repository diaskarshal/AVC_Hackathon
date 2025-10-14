import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import Button from "../components/Button";
import { projectsAPI, Project } from "../services/API";

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
    status: "planning",
    start_date: "",
    planned_end_date: "",
    total_budget: 0,
    location: "",
  });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const response = await projectsAPI.getAll();
      setProjects(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch projects");
    } finally {
      setLoading(false);
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
      const submitData = {
        ...formData,
        total_budget: parseFloat(formData.total_budget.toString()),
        start_date: formData.start_date ? new Date(formData.start_date).toISOString() : undefined,
        planned_end_date: formData.planned_end_date ? new Date(formData.planned_end_date).toISOString() : undefined,
      };

      if (editingProject) {
        await projectsAPI.update(editingProject.id, submitData);
      } else {
        await projectsAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchProjects();
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message || "Failed to save project");
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this project? This will also delete all associated tasks, resources, and budgets.")) {
      try {
        await projectsAPI.delete(id);
        setIsDetailModalOpen(false);
        fetchProjects();
      } catch (err: any) {
        alert(err.message || "Failed to delete project");
      }
    }
  };

  const openCreateModal = () => {
    resetForm();
    setIsModalOpen(true);
  };

  const openEditModal = (project: Project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description || "",
      status: project.status,
      start_date: project.start_date?.split("T")[0] || "",
      planned_end_date: project.planned_end_date?.split("T")[0] || "",
      total_budget: project.total_budget,
      location: project.location || "",
    });
    setIsDetailModalOpen(false);
    setIsModalOpen(true);
  };

  const openDetailModal = (project: Project) => {
    setSelectedProject(project);
    setIsDetailModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
      status: "planning",
      start_date: "",
      planned_end_date: "",
      total_budget: 0,
      location: "",
    });
    setEditingProject(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      planning: "bg-gray-100 text-gray-800",
      in_progress: "bg-blue-100 text-blue-800",
      on_hold: "bg-yellow-100 text-yellow-800",
      completed: "bg-green-100 text-green-800",
      cancelled: "bg-red-100 text-red-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
    }).format(amount);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading projects...</div>
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
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <Button onClick={openCreateModal}>New Project</Button>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <Card key={project.id} className="cursor-pointer hover:shadow-lg transition-shadow">
            <CardBody className="space-y-4">
              <div onClick={() => openDetailModal(project)}>
                <div className="text-lg font-semibold text-gray-900 hover:text-primary-600">
                  {project.name}
                </div>
                <p className="mt-1 text-sm text-gray-500 line-clamp-2">
                  {project.description}
                </p>
              </div>

              <div>
                <span
                  className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(project.status)}`}
                >
                  {project.status.replace("_", " ")}
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Budget:</span>
                  <span className="font-medium text-gray-900">
                    {formatCurrency(project.total_budget)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Spent:</span>
                  <span className="font-medium text-gray-900">
                    {formatCurrency(project.spent_amount)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      project.budget_utilization > 90
                        ? "bg-red-500"
                        : project.budget_utilization > 75
                          ? "bg-yellow-500"
                          : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(project.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
                <div className="text-xs text-gray-500 text-right">
                  {project.budget_utilization.toFixed(1)}% utilized
                </div>
              </div>

              {project.location && (
                <div className="text-sm text-gray-500">
                  📍 {project.location}
                </div>
              )}
            </CardBody>
          </Card>
        ))}
      </div>

      {projects.length === 0 && (
        <Card>
          <CardBody className="text-center py-12">
            <p className="text-gray-500">No projects found</p>
            <Button onClick={openCreateModal} className="mt-4">
              Create Your First Project
            </Button>
          </CardBody>
        </Card>
      )}

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingProject ? "Edit Project" : "Create New Project"}
        size="lg"
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Project Name"
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

          <Select
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleInputChange}
            options={[
              { value: "planning", label: "Planning" },
              { value: "in_progress", label: "In Progress" },
              { value: "on_hold", label: "On Hold" },
              { value: "completed", label: "Completed" },
              { value: "cancelled", label: "Cancelled" },
            ]}
            required
          />

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
            label="Total Budget"
            type="number"
            name="total_budget"
            value={formData.total_budget}
            onChange={handleInputChange}
            placeholder="0.00"
            required
          />

          <Input
            label="Location"
            name="location"
            value={formData.location}
            onChange={handleInputChange}
            placeholder="Project location"
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
              {editingProject ? "Update Project" : "Create Project"}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Project Detail Modal */}
      <Modal
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
        title={selectedProject?.name || "Project Details"}
        size="xl"
      >
        {selectedProject && (
          <div className="space-y-6">
            <div>
              <h4 className="text-sm font-medium text-gray-500">Description</h4>
              <p className="mt-1 text-gray-900">{selectedProject.description || "No description"}</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Status</h4>
                <span
                  className={`mt-1 inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(selectedProject.status)}`}
                >
                  {selectedProject.status.replace("_", " ")}
                </span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500">Location</h4>
                <p className="mt-1 text-gray-900">{selectedProject.location || "N/A"}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Start Date</h4>
                <p className="mt-1 text-gray-900">{formatDate(selectedProject.start_date)}</p>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-500">Planned End Date</h4>
                <p className="mt-1 text-gray-900">{formatDate(selectedProject.planned_end_date)}</p>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">Budget Information</h4>
              <div className="mt-2 space-y-2">
                <div className="flex justify-between">
                  <span>Total Budget:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.total_budget)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Spent Amount:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.spent_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Remaining:</span>
                  <span className="font-semibold">{formatCurrency(selectedProject.remaining_budget)}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      selectedProject.budget_utilization > 90
                        ? "bg-red-500"
                        : selectedProject.budget_utilization > 75
                          ? "bg-yellow-500"
                          : "bg-green-500"
                    }`}
                    style={{
                      width: `${Math.min(selectedProject.budget_utilization, 100)}%`,
                    }}
                  ></div>
                </div>
                <div className="text-sm text-gray-500 text-right">
                  {selectedProject.budget_utilization.toFixed(1)}% utilized
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-3 pt-4 border-t">
              <Button
                variant="secondary"
                onClick={() => setIsDetailModalOpen(false)}
              >
                Close
              </Button>
              <Button
                variant="primary"
                onClick={() => openEditModal(selectedProject)}
              >
                Edit Project
              </Button>
              <Button
                variant="danger"
                onClick={() => handleDelete(selectedProject.id)}
              >
                Delete Project
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Projects;