import React, { useEffect, useState } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import { Table, TableHeader, TableBody, TableHead, TableCell } from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import { exportToCSV } from '../utils/export';
import { resourcesAPI, projectsAPI, Resource, Project } from "../services/API";

const Resources: React.FC = () => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingResource, setEditingResource] = useState<Resource | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");
  const [filterType, setFilterType] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    name: "",
    resource_type: "material",
    status: "available",
    quantity: 0,
    unit: "",
    unit_cost: 0,
    supplier: "",
  });

  useEffect(() => {
    fetchResources();
    fetchProjects();
  }, []);

  const fetchResources = async () => {
    try {
      setLoading(true);
      const response = await resourcesAPI.getAll();
      setResources(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch resources");
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
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  try {
    const submitData = {
      ...formData,
      project_id: parseInt(formData.project_id),
      quantity: parseFloat(formData.quantity.toString()),
      unit_cost: parseFloat(formData.unit_cost.toString()),
    };

    if (editingResource) {
      await resourcesAPI.update(editingResource.id, submitData);
    } else {
      await resourcesAPI.create(submitData);
    }
    setIsModalOpen(false);
    resetForm();
    fetchResources();
  } catch (err: any) {
    alert(err.message || "Failed to save resource");
  }
};

  const handleDelete = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this resource?")) {
      try {
        await resourcesAPI.delete(id);
        fetchResources();
      } catch (err: any) {
        alert(err.message || "Failed to delete resource");
      }
    }
  };

  const handleExport = () => {
    const exportData = filteredResources.map((resource) => ({
      ID: resource.id,
      "Project ID": resource.project_id,
      Name: resource.name,
      Type: resource.resource_type,
      Status: resource.status,
      Quantity: resource.quantity,
      Unit: resource.unit || "N/A",
      "Unit Cost": resource.unit_cost,
      "Total Cost": resource.total_cost,
      Supplier: resource.supplier || "N/A",
      "Allocated Date": new Date(resource.allocated_date).toLocaleDateString(),
    }));

    exportToCSV(exportData, "resources");
  };

  const openEditModal = (resource: Resource) => {
    setEditingResource(resource);
    setFormData({
      project_id: resource.project_id.toString(),
      name: resource.name,
      resource_type: resource.resource_type,
      status: resource.status,
      quantity: resource.quantity,
      unit: resource.unit || "",
      unit_cost: resource.unit_cost,
      supplier: resource.supplier || "",
    });
    setIsModalOpen(true);
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      name: "",
      resource_type: "material",
      status: "available",
      quantity: 0,
      unit: "",
      unit_cost: 0,
      supplier: "",
    });
    setEditingResource(null);
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      available: "bg-green-100 text-green-800",
      in_use: "bg-blue-100 text-blue-800",
      depleted: "bg-red-100 text-red-800",
      maintenance: "bg-yellow-100 text-yellow-800",
    };
    return colors[status] || "bg-gray-100 text-gray-800";
  };

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      material: "🧱",
      equipment: "⚙️",
      labor: "👷",
    };
    return icons[type] || "📦";
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const filteredResources = resources.filter((resource) => {
    if (filterProject && resource.project_id.toString() !== filterProject) return false;
    if (filterType && resource.resource_type !== filterType) return false;
    return true;
  });

  // Calculate totals
  const totalCost = filteredResources.reduce((sum, r) => sum + r.total_cost, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading resources...</div>
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
        <h1 className="text-3xl font-bold text-gray-900">Resources</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            Add New Resource
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Resources</div>
            <div className="text-2xl font-bold text-gray-900">{filteredResources.length}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Cost</div>
            <div className="text-2xl font-bold text-gray-900">{formatCurrency(totalCost)}</div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Available Resources</div>
            <div className="text-2xl font-bold text-gray-900">
              {filteredResources.filter((r) => r.status === "available").length}
            </div>
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
              label="Filter by Type"
              name="filterType"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              options={[
                { value: "", label: "All Types" },
                { value: "material", label: "Material" },
                { value: "equipment", label: "Equipment" },
                { value: "labor", label: "Labor" },
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => {
                  setFilterProject("");
                  setFilterType("");
                }}
                className="w-full"
              >
                Clear Filters
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Resources Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Resource</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Quantity</TableHead>
            <TableHead>Unit Cost</TableHead>
            <TableHead>Total Cost</TableHead>
            <TableHead>Supplier</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredResources.map((resource) => (
              <tr key={resource.id}>
                <TableCell>
                  <div className="flex items-center">
                    <span className="text-2xl mr-2">{getTypeIcon(resource.resource_type)}</span>
                    <div className="font-medium text-gray-900">{resource.name}</div>
                  </div>
                </TableCell>
                <TableCell>
                  {projects.find((p) => p.id === resource.project_id)?.name || `Project #${resource.project_id}`}
                </TableCell>
                <TableCell>
                  <span className="capitalize">{resource.resource_type}</span>
                </TableCell>
                <TableCell>
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(resource.status)}`}
                  >
                    {resource.status.replace("_", " ")}
                  </span>
                </TableCell>
                <TableCell>
                  {resource.quantity} {resource.unit}
                </TableCell>
                <TableCell>{formatCurrency(resource.unit_cost)}</TableCell>
                <TableCell>
                  <span className="font-semibold">{formatCurrency(resource.total_cost)}</span>
                </TableCell>
                <TableCell>
                  {resource.supplier || <span className="text-gray-400">N/A</span>}
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(resource)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(resource.id)}
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
        {filteredResources.length === 0 && (
          <div className="text-center py-12 text-gray-500">No resources found</div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingResource ? "Edit Resource" : "Add New Resource"}
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
            label="Resource Name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />

          <div className="grid grid-cols-2 gap-4">
            <Select
              label="Type"
              name="resource_type"
              value={formData.resource_type}
              onChange={handleInputChange}
              options={[
                { value: "material", label: "Material" },
                { value: "equipment", label: "Equipment" },
                { value: "labor", label: "Labor" },
              ]}
              required
            />

            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleInputChange}
              options={[
                { value: "available", label: "Available" },
                { value: "in_use", label: "In Use" },
                { value: "depleted", label: "Depleted" },
                { value: "maintenance", label: "Maintenance" },
              ]}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Quantity"
              type="number"
              name="quantity"
              value={formData.quantity}
              onChange={handleInputChange}
              required
            />

            <Input
              label="Unit"
              name="unit"
              value={formData.unit}
              onChange={handleInputChange}
              placeholder="kg, m³, hours, etc."
            />
          </div>

          <Input
            label="Unit Cost"
            type="number"
            name="unit_cost"
            value={formData.unit_cost}
            onChange={handleInputChange}
            placeholder="0.00"
            required
          />

          <Input
            label="Supplier"
            name="supplier"
            value={formData.supplier}
            onChange={handleInputChange}
            placeholder="Supplier name"
          />

          <div className="bg-gray-50 px-4 py-3 rounded">
            <div className="text-sm text-gray-600">
              Total Cost:{" "}
              <span className="font-semibold text-gray-900">
                {formatCurrency(Number(formData.quantity) * Number(formData.unit_cost))}
              </span>
            </div>
          </div>

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
              {editingResource ? "Update Resource" : "Add Resource"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Resources;