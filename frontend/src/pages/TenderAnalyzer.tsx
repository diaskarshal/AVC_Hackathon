import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Button from "../components/Button";
import api from "../services/API";

interface TenderListItem {
  id: number;
  title: string;
  status: string;
  file_name: string;
  created_at: string;
  parsed_scope: any;
  created_project_id: number | null;
}

interface ResourceItem {
  resource_type: string;
  name: string;
  quantity: number;
  unit: string;
  unit_cost: number;
  total_cost: number;
  notes?: string;
}

interface TaskItem {
  name: string;
  description: string;
  duration_days: number;
  priority: string;
  assigned_role?: string;
}

interface SimilarProject {
  id: number;
  name: string;
  score: number;
}

interface LotItem {
  lot_number: string;
  name: string;
  description: string;
  quantity: number;
  unit: string;
  planned_amount_kzt: number;
  location: string;
  deadline: string;
}

interface AnalysisResult {
  tender_id: number;
  parsed_scope: any;
  plan_id: number;
  estimated_total_cost: number;
  estimated_duration_days: number;
  resources: ResourceItem[];
  tasks: TaskItem[];
  similar_projects: SimilarProject[];
  reasoning: string;
  confidence_score: number;
  specialists_count: number;
  equipment_count: number;
  total_manhours: number;
}

type Step = "upload" | "analyzing" | "results" | "accepted";

const TenderAnalyzer: React.FC = () => {
  const [step, setStep] = useState<Step>("upload");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tenderId, setTenderId] = useState<number | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [tenders, setTenders] = useState<TenderListItem[]>([]);
  const [createdProjectId, setCreatedProjectId] = useState<number | null>(null);
  const [projectName, setProjectName] = useState("");

  // Editable plan state
  const [editResources, setEditResources] = useState<ResourceItem[]>([]);
  const [editTasks, setEditTasks] = useState<TaskItem[]>([]);

  useEffect(() => {
    loadTenders();
  }, []);

  const loadTenders = async () => {
    try {
      const res = await api.get("/api/tender/");
      setTenders(res.data);
    } catch {
      // ignore
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select a file");
      return;
    }
    setError(null);
    setStep("analyzing");

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      const uploadRes = await api.post("/api/tender/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const tid = uploadRes.data.tender_id;
      setTenderId(tid);

      const analyzeRes = await api.post(`/api/tender/${tid}/analyze`);
      setAnalysis(analyzeRes.data);
      setEditResources(analyzeRes.data.resources || []);
      setEditTasks(analyzeRes.data.tasks || []);
      const scope = analyzeRes.data.parsed_scope;
      setProjectName(scope?.title || scope?.work_type || selectedFile.name.replace(/\.(pdf|xlsx|xls|txt)$/i, ""));
      setStep("results");
      loadTenders();
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Analysis failed");
      setStep("upload");
    }
  };

  const handleReanalyze = async (tid: number) => {
    setError(null);
    setStep("analyzing");
    setTenderId(tid);

    try {
      const analyzeRes = await api.post(`/api/tender/${tid}/analyze`);
      setAnalysis(analyzeRes.data);
      setEditResources(analyzeRes.data.resources || []);
      setEditTasks(analyzeRes.data.tasks || []);
      const rScope = analyzeRes.data.parsed_scope;
      setProjectName(rScope?.title || rScope?.work_type || "New Project");
      setStep("results");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Re-analysis failed");
      setStep("upload");
    }
  };

  const handleDeleteTender = async (tid: number) => {
    if (!window.confirm("Delete this tender and its analysis?")) return;
    try {
      await api.delete(`/api/tender/${tid}`);
      loadTenders();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to delete tender");
    }
  };

  const handleAccept = async () => {
    if (!tenderId || !analysis) return;
    setError(null);

    try {
      const res = await api.post(`/api/tender/${tenderId}/accept`, {
        plan_id: analysis.plan_id,
        project_name: projectName || undefined,
        resources: editResources,
        tasks: editTasks,
      });
      setCreatedProjectId(res.data.project_id);
      setStep("accepted");
      loadTenders();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to create project");
    }
  };

  const formatCost = (cost: number) =>
    new Intl.NumberFormat("ru-RU").format(Math.round(cost)) + " KZT";

  const calcTotal = (items: ResourceItem[]) =>
    items.reduce((sum, r) => sum + r.quantity * r.unit_cost, 0);

  const resetToUpload = () => {
    setStep("upload");
    setSelectedFile(null);
    setAnalysis(null);
    setTenderId(null);
    setCreatedProjectId(null);
    setError(null);
    setProjectName("");
    setEditResources([]);
    setEditTasks([]);
  };

  // ── Resource row helpers ──────────────────────────────────────────────────
  const updateResource = (idx: number, field: keyof ResourceItem, value: any) => {
    setEditResources((prev) => {
      const next = [...prev];
      next[idx] = { ...next[idx], [field]: value };
      if (field === "quantity" || field === "unit_cost") {
        next[idx].total_cost = next[idx].quantity * next[idx].unit_cost;
      }
      return next;
    });
  };

  const deleteResource = (idx: number) =>
    setEditResources((prev) => prev.filter((_, i) => i !== idx));

  const addResource = () =>
    setEditResources((prev) => [
      ...prev,
      { resource_type: "material", name: "", quantity: 1, unit: "шт", unit_cost: 0, total_cost: 0 },
    ]);

  // ── Task row helpers ──────────────────────────────────────────────────────
  const updateTask = (idx: number, field: keyof TaskItem, value: any) => {
    setEditTasks((prev) => {
      const next = [...prev];
      next[idx] = { ...next[idx], [field]: value };
      return next;
    });
  };

  const deleteTask = (idx: number) =>
    setEditTasks((prev) => prev.filter((_, i) => i !== idx));

  const addTask = () =>
    setEditTasks((prev) => [
      ...prev,
      { name: "", description: "", duration_days: 7, priority: "medium", assigned_role: "" },
    ]);

  const inputCls =
    "w-full border border-gray-300 rounded px-2 py-1 text-sm focus:ring-1 focus:ring-primary-500 focus:border-primary-500";

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tender Analyzer</h1>
        {step !== "upload" && (
          <Button variant="secondary" onClick={resetToUpload}>
            New Analysis
          </Button>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* ── Step 1: Upload ───────────────────────────────────────────────── */}
      {step === "upload" && (
        <>
          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium text-gray-900">Upload Tender Document</h3>
            </CardHeader>
            <CardBody className="space-y-4">
              <p className="text-sm text-gray-600">
                Upload a tender document (PDF or Excel) from Goszakup or Samruk-Kazyna. The
                system will extract scope using AI, find similar historical projects, and
                generate a resource plan you can edit before accepting.
              </p>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8">
                <div className="text-center">
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <div className="mt-4">
                    <label
                      htmlFor="tender-upload"
                      className="cursor-pointer font-medium text-primary-600 hover:text-primary-500"
                    >
                      <span>Choose a tender file</span>
                      <input
                        id="tender-upload"
                        type="file"
                        className="sr-only"
                        accept=".pdf,.xlsx,.xls,.txt"
                        onChange={handleFileChange}
                      />
                    </label>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">PDF, Excel, or TXT up to 10MB</p>
                </div>
              </div>

              {selectedFile && (
                <div className="flex items-center justify-between bg-gray-50 p-4 rounded-md">
                  <div className="flex items-center">
                    <span className="text-sm font-medium text-gray-900">{selectedFile.name}</span>
                    <span className="ml-2 text-xs text-gray-500">
                      ({(selectedFile.size / 1024).toFixed(1)} KB)
                    </span>
                  </div>
                  <Button variant="secondary" size="sm" onClick={() => setSelectedFile(null)}>
                    Remove
                  </Button>
                </div>
              )}

              <div className="flex justify-end">
                <Button onClick={handleUploadAndAnalyze} disabled={!selectedFile} size="lg">
                  Upload & Analyze
                </Button>
              </div>
            </CardBody>
          </Card>

          {/* Previous tenders */}
          {tenders.length > 0 && (
            <Card>
              <CardHeader>
                <h3 className="text-lg font-medium text-gray-900">Previous Tenders</h3>
              </CardHeader>
              <CardBody>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {tenders.map((t) => (
                        <tr key={t.id}>
                          <td className="px-4 py-3 text-sm text-gray-900">{t.title}</td>
                          <td className="px-4 py-3 text-sm text-gray-500">{t.file_name}</td>
                          <td className="px-4 py-3">
                            <span
                              className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                t.status === "accepted"
                                  ? "bg-green-100 text-green-800"
                                  : t.status === "plan_generated"
                                  ? "bg-blue-100 text-blue-800"
                                  : t.status === "parsed"
                                  ? "bg-yellow-100 text-yellow-800"
                                  : "bg-gray-100 text-gray-800"
                              }`}
                            >
                              {t.status}
                            </span>
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-500">
                            {t.created_at ? new Date(t.created_at).toLocaleDateString() : ""}
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              {t.status !== "accepted" && (
                                <Button size="sm" onClick={() => handleReanalyze(t.id)}>
                                  Analyze
                                </Button>
                              )}
                              {t.created_project_id && (
                                <span className="text-sm text-green-600">
                                  Project #{t.created_project_id}
                                </span>
                              )}
                              <Button
                                size="sm"
                                variant="danger"
                                onClick={() => handleDeleteTender(t.id)}
                              >
                                Delete
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardBody>
            </Card>
          )}
        </>
      )}

      {/* ── Step 2: Analyzing ────────────────────────────────────────────── */}
      {step === "analyzing" && (
        <Card>
          <CardBody>
            <div className="text-center py-16">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4" />
              <p className="text-lg font-medium text-gray-900">
                Analyzing tender document...
              </p>
              <p className="text-sm text-gray-500 mt-2">
                AI is extracting scope, finding similar projects, and generating a resource plan.
                This may take 10–20 seconds.
              </p>
            </div>
          </CardBody>
        </Card>
      )}

      {/* ── Step 3: Results (editable tables) ───────────────────────────── */}
      {step === "results" && analysis && (
        <>
          {/* Summary cards */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Parsed Scope — shows raw lot data from the tender table */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-medium text-gray-900">Parsed Scope</h3>
              </CardHeader>
              <CardBody>
                {(() => {
                  const lots: LotItem[] = analysis.parsed_scope?.lots || [];
                  if (lots.length === 0) {
                    return (
                      <p className="text-sm text-gray-400 italic">
                        No lot data extracted. Check parser or PDF format.
                      </p>
                    );
                  }
                  return (
                    <div className="space-y-4">
                      {lots.map((lot, i) => (
                        <div key={i} className="space-y-2">
                          {lots.length > 1 && (
                            <p className="text-xs font-bold text-gray-400 uppercase">
                              Лот {lot.lot_number}
                            </p>
                          )}
                          <div>
                            <span className="text-xs font-medium text-gray-500 uppercase">
                              Наименование и краткая характеристика
                            </span>
                            <p className="text-sm text-gray-900 mt-0.5">{lot.name || "—"}</p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-gray-500 uppercase">
                              Дополнительная характеристика
                            </span>
                            <p className="text-sm text-gray-900 mt-0.5">{lot.description || "—"}</p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-gray-500 uppercase">
                              Планируемая сумма без НДС
                            </span>
                            <p className="text-sm font-semibold text-gray-900 mt-0.5">
                              {lot.planned_amount_kzt
                                ? formatCost(lot.planned_amount_kzt)
                                : "—"}
                            </p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-gray-500 uppercase">
                              Место поставки / выполнения работ
                            </span>
                            <p className="text-sm text-gray-900 mt-0.5">{lot.location || "—"}</p>
                          </div>
                          <div>
                            <span className="text-xs font-medium text-gray-500 uppercase">
                              Требуемый срок
                            </span>
                            <p className="text-sm text-gray-900 mt-0.5">{lot.deadline || "—"}</p>
                          </div>
                          {lot.quantity > 0 && (
                            <div>
                              <span className="text-xs font-medium text-gray-500 uppercase">
                                Кол-во / Ед. изм.
                              </span>
                              <p className="text-sm text-gray-900 mt-0.5">
                                {lot.quantity} {lot.unit}
                              </p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  );
                })()}
              </CardBody>
            </Card>

            {/* Similar Projects */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-medium text-gray-900">Similar Projects</h3>
              </CardHeader>
              <CardBody className="space-y-3">
                {analysis.similar_projects.length === 0 ? (
                  <p className="text-sm text-gray-500">No similar projects found.</p>
                ) : (
                  analysis.similar_projects.map((sp, i) => (
                    <div key={i} className="border rounded-lg p-3 bg-gray-50">
                      <div className="flex justify-between items-start">
                        <p className="text-sm font-medium text-gray-900">{sp.name}</p>
                        <span
                          className={`text-xs font-bold px-2 py-1 rounded-full ${
                            sp.score >= 0.7
                              ? "bg-green-100 text-green-800"
                              : sp.score >= 0.4
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-gray-100 text-gray-600"
                          }`}
                        >
                          {(sp.score * 100).toFixed(0)}% match
                        </span>
                      </div>
                    </div>
                  ))
                )}
                {analysis.confidence_score > 0 && (
                  <div className="text-center mt-2">
                    <span className="text-xs text-gray-500">
                      Confidence: {(analysis.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                )}
              </CardBody>
            </Card>

            {/* AI Reasoning — workforce estimate */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-medium text-gray-900">AI Analysis</h3>
              </CardHeader>
              <CardBody>
                <div className="bg-blue-50 rounded-lg p-4">
                  <p className="text-sm font-bold text-blue-800 mb-3 tracking-wide">
                    ВСЕГО ЗАДЕЙСТВОВАНО:
                  </p>
                  <div className="space-y-2">
                    <p className="text-base text-blue-900">
                      <span className="font-bold text-lg">
                        {(analysis.specialists_count || 0).toLocaleString("ru-RU")}
                      </span>
                      {" "}– специалистов
                    </p>
                    <p className="text-base text-blue-900">
                      <span className="font-bold text-lg">
                        {(analysis.equipment_count || 0).toLocaleString("ru-RU")}
                      </span>
                      {" "}– единиц техники
                    </p>
                    <p className="text-base text-blue-900">
                      <span className="font-bold text-lg">
                        {(analysis.total_manhours || 0).toLocaleString("ru-RU")}
                      </span>
                      {" "}– чел/часов
                    </p>
                  </div>
                </div>
              </CardBody>
            </Card>
          </div>

          {/* ── Editable Resource Plan ───────────────────────────────────── */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">
                  Resource Plan{" "}
                  <span className="text-sm font-normal text-gray-500">(editable)</span>
                </h3>
                <span className="text-sm text-gray-500">
                  Total:{" "}
                  <span className="font-bold text-gray-900">
                    {formatCost(calcTotal(editResources))}
                  </span>
                </span>
              </div>
            </CardHeader>
            <CardBody>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Type
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Name
                      </th>
                      <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase w-20">
                        Qty
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase w-20">
                        Unit
                      </th>
                      <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase w-32">
                        Unit Cost
                      </th>
                      <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase w-32">
                        Total
                      </th>
                      <th className="px-3 py-3 w-8"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {editResources.map((r, i) => (
                      <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="px-3 py-2">
                          <select
                            value={r.resource_type}
                            onChange={(e) =>
                              updateResource(i, "resource_type", e.target.value)
                            }
                            className="border border-gray-300 rounded px-1 py-1 text-xs"
                          >
                            <option value="labor">labor</option>
                            <option value="material">material</option>
                            <option value="equipment">equipment</option>
                          </select>
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="text"
                            value={r.name}
                            onChange={(e) => updateResource(i, "name", e.target.value)}
                            className={inputCls}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="number"
                            value={r.quantity}
                            min={0}
                            onChange={(e) =>
                              updateResource(i, "quantity", parseFloat(e.target.value) || 0)
                            }
                            className={inputCls + " text-right"}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="text"
                            value={r.unit}
                            onChange={(e) => updateResource(i, "unit", e.target.value)}
                            className={inputCls}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="number"
                            value={r.unit_cost}
                            min={0}
                            onChange={(e) =>
                              updateResource(i, "unit_cost", parseFloat(e.target.value) || 0)
                            }
                            className={inputCls + " text-right"}
                          />
                        </td>
                        <td className="px-3 py-2 text-sm font-medium text-gray-900 text-right whitespace-nowrap">
                          {formatCost(r.quantity * r.unit_cost)}
                        </td>
                        <td className="px-3 py-2 text-center">
                          <button
                            onClick={() => deleteResource(i)}
                            className="text-red-400 hover:text-red-600 font-bold"
                            title="Remove row"
                          >
                            ✕
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="mt-3">
                <Button variant="secondary" size="sm" onClick={addResource}>
                  + Add Resource
                </Button>
              </div>
            </CardBody>
          </Card>

          {/* ── Editable Task Plan ───────────────────────────────────────── */}
          <Card>
            <CardHeader>
              <h3 className="text-lg font-medium text-gray-900">
                Task Plan{" "}
                <span className="text-sm font-normal text-gray-500">(editable)</span>
              </h3>
            </CardHeader>
            <CardBody>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        #
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Task Name
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Description
                      </th>
                      <th className="px-3 py-3 text-right text-xs font-medium text-gray-500 uppercase w-24">
                        Days
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase w-28">
                        Priority
                      </th>
                      <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                        Role
                      </th>
                      <th className="px-3 py-3 w-8"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {editTasks.map((t, i) => (
                      <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="px-3 py-2 text-sm text-gray-500">{i + 1}</td>
                        <td className="px-3 py-2">
                          <input
                            type="text"
                            value={t.name}
                            onChange={(e) => updateTask(i, "name", e.target.value)}
                            className={inputCls}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="text"
                            value={t.description}
                            onChange={(e) => updateTask(i, "description", e.target.value)}
                            className={inputCls}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="number"
                            value={t.duration_days}
                            min={1}
                            onChange={(e) =>
                              updateTask(i, "duration_days", parseInt(e.target.value) || 1)
                            }
                            className={inputCls + " text-right"}
                          />
                        </td>
                        <td className="px-3 py-2">
                          <select
                            value={t.priority}
                            onChange={(e) => updateTask(i, "priority", e.target.value)}
                            className="border border-gray-300 rounded px-1 py-1 text-xs"
                          >
                            <option value="high">high</option>
                            <option value="medium">medium</option>
                            <option value="low">low</option>
                          </select>
                        </td>
                        <td className="px-3 py-2">
                          <input
                            type="text"
                            value={t.assigned_role || ""}
                            onChange={(e) => updateTask(i, "assigned_role", e.target.value)}
                            className={inputCls}
                          />
                        </td>
                        <td className="px-3 py-2 text-center">
                          <button
                            onClick={() => deleteTask(i)}
                            className="text-red-400 hover:text-red-600 font-bold"
                            title="Remove row"
                          >
                            ✕
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div className="mt-3">
                <Button variant="secondary" size="sm" onClick={addTask}>
                  + Add Task
                </Button>
              </div>
            </CardBody>
          </Card>

          {/* ── Accept Section ───────────────────────────────────────────── */}
          <Card>
            <CardBody>
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Project Name
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-primary-500 focus:border-primary-500"
                    placeholder="Enter project name..."
                  />
                </div>
                <Button size="lg" variant="success" onClick={handleAccept}>
                  Accept & Create Project
                </Button>
              </div>
            </CardBody>
          </Card>
        </>
      )}

      {/* ── Step 4: Accepted ─────────────────────────────────────────────── */}
      {step === "accepted" && (
        <Card>
          <CardBody>
            <div className="text-center py-12">
              <div className="mx-auto h-16 w-16 text-green-500 mb-4">
                <svg
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Project Created Successfully!
              </h3>
              <p className="text-gray-600 mb-6">
                Project #{createdProjectId} has been created with {editResources.length}{" "}
                resources and {editTasks.length} tasks.
              </p>
              <div className="flex justify-center space-x-4">
                <Button onClick={resetToUpload}>Analyze Another Tender</Button>
                <Button
                  variant="secondary"
                  onClick={() => (window.location.href = "/projects")}
                >
                  View Projects
                </Button>
              </div>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
};

export default TenderAnalyzer;
