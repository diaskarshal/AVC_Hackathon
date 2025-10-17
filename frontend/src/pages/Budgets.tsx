import React, { useEffect, useState } from "react";
import { Card, CardBody } from "../components/Card";
// import { Card, CardHeader, CardBody } from "../components/Card";
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableCell,
} from "../components/Table";
import Button from "../components/Button";
import Modal from "../components/Modal";
import Input from "../components/Input";
import Select from "../components/Select";
import TextArea from "../components/TextArea";
import { exportToCSV } from '../utils/export';
import { budgetsAPI, projectsAPI, Budget, Project } from "../services/API";

const Budgets: React.FC = () => {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingBudget, setEditingBudget] = useState<Budget | null>(null);
  const [filterProject, setFilterProject] = useState<string>("");

  const [formData, setFormData] = useState({
    project_id: "",
    category: "",
    description: "",
    planned_amount: 0,
    actual_amount: 0,
  });

  useEffect(() => {
    fetchBudgets();
    fetchProjects();
  }, []);

  const fetchBudgets = async () => {
    try {
      setLoading(true);
      const response = await budgetsAPI.getAll();
      setBudgets(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to fetch budgets");
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
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
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
        planned_amount: parseFloat(formData.planned_amount.toString()),
        actual_amount: parseFloat(formData.actual_amount.toString()),
      };

      if (editingBudget) {
        await budgetsAPI.update(editingBudget.id, submitData);
      } else {
        await budgetsAPI.create(submitData);
      }
      setIsModalOpen(false);
      resetForm();
      fetchBudgets();
    } catch (err: any) {
      alert(err.message || "Failed to save budget");
    }
  };

  const handleDelete = async (id: number) => {
    if (
      window.confirm("Are you sure you want to delete this budget entry?")
    ) {
      try {
        await budgetsAPI.delete(id);
        fetchBudgets();
      } catch (err: any) {
        alert(err.message || "Failed to delete budget");
      }
    }
  };

  const openEditModal = (budget: Budget) => {
    setEditingBudget(budget);
    setFormData({
      project_id: budget.project_id.toString(),
      category: budget.category,
      description: budget.description || "",
      planned_amount: budget.planned_amount,
      actual_amount: budget.actual_amount,
    });
    setIsModalOpen(true);
  };

  const handleExport = () => {
    const exportData = filteredBudgets.map((budget) => ({
      ID: budget.id,
      "Project ID": budget.project_id,
      Category: budget.category,
      Description: budget.description || "N/A",
      "Planned Amount": budget.planned_amount,
      "Actual Amount": budget.actual_amount,
      Variance: budget.variance,
      "Variance %": budget.variance_percentage.toFixed(2),
      Date: new Date(budget.budget_date).toLocaleDateString(),
    }));

    exportToCSV(exportData, "budgets");
  };

  const resetForm = () => {
    setFormData({
      project_id: "",
      category: "",
      description: "",
      planned_amount: 0,
      actual_amount: 0,
    });
    setEditingBudget(null);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  };

  const getVarianceColor = (variance: number) => {
    if (variance > 0) return "text-green-600";
    if (variance < 0) return "text-red-600";
    return "text-gray-600";
  };

  const filteredBudgets = budgets.filter((budget) => {
    if (filterProject && budget.project_id.toString() !== filterProject)
      return false;
    return true;
  });

  // Calculate totals
  const totalPlanned = filteredBudgets.reduce(
    (sum, b) => sum + b.planned_amount,
    0
  );
  const totalActual = filteredBudgets.reduce(
    (sum, b) => sum + b.actual_amount,
    0
  );
  const totalVariance = totalPlanned - totalActual;
  const variancePercentage =
    totalPlanned > 0 ? (totalVariance / totalPlanned) * 100 : 0;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading budgets...</div>
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
        <h1 className="text-3xl font-bold text-gray-900">Budgets</h1>
        <div className="flex space-x-3">
          <Button variant="secondary" onClick={handleExport}>
            📥 Export
          </Button>
          <Button onClick={() => setIsModalOpen(true)}>
            Add Budget Entry
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Planned</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalPlanned)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Total Actual</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(totalActual)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Variance</div>
            <div
              className={`text-2xl font-bold ${getVarianceColor(totalVariance)}`}
            >
              {formatCurrency(totalVariance)}
            </div>
          </CardBody>
        </Card>
        <Card>
          <CardBody>
            <div className="text-sm text-gray-500">Variance %</div>
            <div
              className={`text-2xl font-bold ${getVarianceColor(totalVariance)}`}
            >
              {variancePercentage.toFixed(1)}%
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Filter */}
      <Card>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Select
              label="Filter by Project"
              name="filterProject"
              value={filterProject}
              onChange={(e) => setFilterProject(e.target.value)}
              options={[
                { value: "", label: "All Projects" },
                ...projects.map((p) => ({
                  value: p.id.toString(),
                  label: p.name,
                })),
              ]}
            />
            <div className="flex items-end">
              <Button
                variant="secondary"
                onClick={() => setFilterProject("")}
                className="w-full"
              >
                Clear Filter
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Budgets Table */}
      <Card>
        <Table>
          <TableHeader>
            <TableHead>Category</TableHead>
            <TableHead>Project</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Planned Amount</TableHead>
            <TableHead>Actual Amount</TableHead>
            <TableHead>Variance</TableHead>
            <TableHead>Variance %</TableHead>
            <TableHead>Actions</TableHead>
          </TableHeader>
          <TableBody>
            {filteredBudgets.map((budget) => (
              <tr key={budget.id}>
                <TableCell>
                  <div className="font-medium text-gray-900">
                    {budget.category}
                  </div>
                </TableCell>
                <TableCell>
                  {projects.find((p) => p.id === budget.project_id)?.name ||
                    `Project #${budget.project_id}`}
                </TableCell>
                <TableCell>
                  <div className="text-gray-600 max-w-xs truncate">
                    {budget.description || (
                      <span className="text-gray-400">No description</span>
                    )}
                  </div>
                </TableCell>
                <TableCell>
                  <span className="font-semibold">
                    {formatCurrency(budget.planned_amount)}
                  </span>
                </TableCell>
                <TableCell>
                  <span className="font-semibold">
                    {formatCurrency(budget.actual_amount)}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`font-semibold ${getVarianceColor(budget.variance)}`}
                  >
                    {formatCurrency(budget.variance)}
                  </span>
                </TableCell>
                <TableCell>
                  <span
                    className={`font-semibold ${getVarianceColor(budget.variance)}`}
                  >
                    {budget.variance_percentage.toFixed(1)}%
                  </span>
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => openEditModal(budget)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(budget.id)}
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
        {filteredBudgets.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            No budget entries found
          </div>
        )}
      </Card>

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          resetForm();
        }}
        title={editingBudget ? "Edit Budget Entry" : "Add Budget Entry"}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleInputChange}
            options={[
              { value: "", label: "Select a project" },
              ...projects.map((p) => ({
                value: p.id.toString(),
                label: p.name,
              })),
            ]}
            required
          />

          <Input
            label="Category"
            name="category"
            value={formData.category}
            onChange={handleInputChange}
            placeholder="e.g., Materials, Labor, Equipment"
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
            <Input
              label="Planned Amount"
              type="number"
              name="planned_amount"
              value={formData.planned_amount}
              onChange={handleInputChange}
              placeholder="0.00"
              required
            />

            <Input
              label="Actual Amount"
              type="number"
              name="actual_amount"
              value={formData.actual_amount}
              onChange={handleInputChange}
              placeholder="0.00"
              required
            />
          </div>

          <div className="bg-gray-50 px-4 py-3 rounded">
            <div className="text-sm text-gray-600">
              Variance:{" "}
              <span
                className={`font-semibold ${getVarianceColor(
                  parseFloat(formData.planned_amount.toString()) -
                    parseFloat(formData.actual_amount.toString())
                )}`}
              >
                {formatCurrency(
                  parseFloat(formData.planned_amount.toString()) -
                    parseFloat(formData.actual_amount.toString())
                )}
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
              {editingBudget ? "Update Budget" : "Add Budget"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Budgets;