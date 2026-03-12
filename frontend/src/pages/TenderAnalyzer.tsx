import React, { useState, useEffect, useRef } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Button from "../components/Button";
import api, { tenderAPI } from "../services/API";

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

  // Confidence gauge
  const gaugeRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (step !== "results" || !analysis || !gaugeRef.current) return;
    const Plotly = (window as any).Plotly;
    if (!Plotly) return;
    const score = analysis.confidence_score || 0;
    const color = score >= 0.7 ? "#16a34a" : score >= 0.4 ? "#d97706" : "#dc2626";
    Plotly.newPlot(
      gaugeRef.current,
      [{
        type: "indicator",
        mode: "gauge+number",
        value: Math.round(score * 100),
        number: { suffix: "%", font: { size: 28, color } },
        gauge: {
          axis: { range: [0, 100], tickwidth: 1, tickcolor: "#9ca3af" },
          bar: { color, thickness: 0.3 },
          bgcolor: "white",
          borderwidth: 0,
          steps: [
            { range: [0, 40], color: "#fef2f2" },
            { range: [40, 70], color: "#fffbeb" },
            { range: [70, 100], color: "#f0fdf4" },
          ],
        },
      }],
      { margin: { t: 10, b: 5, l: 20, r: 20 }, height: 140, paper_bgcolor: "rgba(0,0,0,0)" },
      { displayModeBar: false, responsive: true }
    );
  }, [step, analysis]);

  // Gantt chart
  const ganttRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (step !== "results" || !ganttRef.current || editTasks.length === 0) return;
    const Plotly = (window as any).Plotly;
    if (!Plotly) return;
    // Build cumulative start days
    const starts: number[] = [];
    let cursor = 0;
    editTasks.forEach((t) => { starts.push(cursor); cursor += t.duration_days; });
    const colorMap: Record<string, string> = { high: "#ef4444", medium: "#f59e0b", low: "#22c55e" };
    const labels = editTasks.map((t) => (t.name.length > 35 ? t.name.slice(0, 33) + "…" : t.name));
    Plotly.newPlot(
      ganttRef.current,
      [{
        type: "bar",
        orientation: "h",
        x: editTasks.map((t) => t.duration_days),
        y: labels,
        base: starts,
        marker: { color: editTasks.map((t) => colorMap[t.priority] ?? "#6366f1") },
        hovertemplate: "<b>%{y}</b><br>Начало: день %{base}<br>Длительность: %{x} дн.<extra></extra>",
        width: 0.6,
      }],
      {
        xaxis: { title: "Дни", zeroline: false, gridcolor: "#e5e7eb" },
        yaxis: { autorange: "reversed", gridcolor: "#e5e7eb" },
        margin: { l: 200, r: 20, t: 10, b: 40 },
        height: Math.max(180, editTasks.length * 38 + 80),
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "#f9fafb",
        bargap: 0.35,
        annotations: [
          { x: 1.01, y: 1.05, xref: "paper", yref: "paper", text: "🔴 Высокий  🟡 Средний  🟢 Низкий", showarrow: false, font: { size: 10, color: "#6b7280" }, align: "right" }
        ],
      },
      { displayModeBar: false, responsive: true }
    );
  }, [step, editTasks]);

  // Hot deals
  const [hotDeals, setHotDeals] = useState<any[]>([]);
  const [hotDealsLoading, setHotDealsLoading] = useState(true);

  const fetchHotDeals = () => {
    setHotDealsLoading(true);
    tenderAPI.getHotDeals()
      .then((res) => setHotDeals(res.data))
      .catch(() => {})
      .finally(() => setHotDealsLoading(false));
  };

  useEffect(() => {
    loadTenders();
    fetchHotDeals();
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

          {/* ── Горячие тендеры ──────────────────────────────────────────── */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <span className="text-orange-500 text-xl">🔥</span>
                <h3 className="text-lg font-medium text-gray-900">Горячие тендеры</h3>
                <button
                  onClick={fetchHotDeals}
                  disabled={hotDealsLoading}
                  className="ml-auto flex items-center gap-1 px-3 py-1 text-xs font-medium rounded-md border border-gray-300 text-gray-600 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  title="Обновить список тендеров"
                >
                  <svg
                    className={`h-3.5 w-3.5 ${hotDealsLoading ? "animate-spin" : ""}`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  Обновить
                </button>
              </div>
            </CardHeader>
            <CardBody>
              {hotDealsLoading ? (
                <div className="text-center text-gray-400 py-6">Загрузка…</div>
              ) : hotDeals.length === 0 ? (
                <div className="text-center text-gray-400 py-6">Актуальных тендеров не найдено</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 text-sm">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">№</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Наименование</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Заказчик</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">Сумма (₸)</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Дедлайн</th>
                        <th className="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase">Источник</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {hotDeals.map((deal, i) => {
                        const daysLeft = deal.deadline
                          ? Math.ceil((new Date(deal.deadline).getTime() - Date.now()) / 86_400_000)
                          : null;
                        return (
                          <tr key={deal.id ?? i} className="hover:bg-orange-50 transition-colors">
                            <td className="px-4 py-3 whitespace-nowrap">
                              {deal.url ? (
                                <a
                                  href={deal.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:text-blue-800 hover:underline font-medium"
                                  title="Открыть на портале"
                                >
                                  {deal.number || `#${i + 1}`}
                                </a>
                              ) : (
                                <span className="text-gray-500">{deal.number || `#${i + 1}`}</span>
                              )}
                            </td>
                            <td className="px-4 py-3 font-medium text-gray-900 max-w-xs">{deal.title}</td>
                            <td className="px-4 py-3 text-gray-600 whitespace-nowrap max-w-[180px] truncate">{deal.company}</td>
                            <td className="px-4 py-3 text-right font-semibold text-gray-900 whitespace-nowrap">
                              {deal.amount_kzt
                                ? new Intl.NumberFormat("ru-RU").format(deal.amount_kzt)
                                : "—"}
                            </td>
                            <td className="px-4 py-3 whitespace-nowrap">
                              {deal.deadline ? (
                                <span className={`inline-flex items-center gap-1 font-medium ${
                                  daysLeft !== null && daysLeft <= 10 ? "text-red-600" :
                                  daysLeft !== null && daysLeft <= 20 ? "text-yellow-600" :
                                  "text-green-600"
                                }`}>
                                  {deal.deadline}
                                  {daysLeft !== null && (
                                    <span className="text-xs font-normal text-gray-400">
                                      ({daysLeft}д)
                                    </span>
                                  )}
                                </span>
                              ) : "—"}
                            </td>
                            <td className="px-4 py-3 text-center">
                              <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                                deal.source === "samruk"
                                  ? "bg-blue-100 text-blue-700"
                                  : "bg-green-100 text-green-700"
                              }`}>
                                {deal.source === "samruk" ? "Самрук" : "Госзакуп"}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
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
                                <>
                                  <Button size="sm" onClick={() => handleReanalyze(t.id)}>
                                    Analyze
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="danger"
                                    onClick={() => handleDeleteTender(t.id)}
                                  >
                                    Delete
                                  </Button>
                                </>
                              )}
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
                <h3 className="text-lg font-medium text-gray-900">Похожие проекты</h3>
              </CardHeader>
              <CardBody className="space-y-3">
                {analysis.similar_projects.length === 0 ? (
                  <div className="text-center py-4">
                    <p className="text-sm text-gray-500">Аналогичных проектов не найдено</p>
                    <p className="text-xs text-gray-400 mt-1">Расчёт выполнен по отраслевым нормативам</p>
                  </div>
                ) : (
                  analysis.similar_projects.map((sp, i) => (
                    <div
                      key={i}
                      className={`border rounded-lg p-3 ${
                        i === 0
                          ? "bg-blue-50 border-blue-200"
                          : "bg-gray-50 border-gray-200"
                      }`}
                    >
                      <div className="flex justify-between items-start gap-2">
                        <div className="flex-1 min-w-0">
                          {i === 0 && (
                            <p className="text-xs font-semibold text-blue-600 uppercase mb-0.5">
                              Основной аналог
                            </p>
                          )}
                          <p className="text-sm font-medium text-gray-900 leading-tight">{sp.name}</p>
                          {i === 0 && (
                            <p className="text-xs text-blue-600 mt-1">
                              На основе данного проекта построен ресурсный план
                            </p>
                          )}
                        </div>
                        <span
                          className={`shrink-0 text-xs font-bold px-2 py-1 rounded-full ${
                            sp.score >= 0.7
                              ? "bg-green-100 text-green-800"
                              : sp.score >= 0.4
                              ? "bg-yellow-100 text-yellow-800"
                              : "bg-gray-100 text-gray-600"
                          }`}
                        >
                          {(sp.score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </CardBody>
            </Card>

            {/* AI Confidence + Stats */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-medium text-gray-900">ИИ Уверенность</h3>
              </CardHeader>
              <CardBody>
                <div ref={gaugeRef} className="w-full" />
                <p className="text-center text-xs text-gray-500 -mt-1 mb-3">
                  {analysis.confidence_score >= 0.7
                    ? "Высокая точность расчёта"
                    : analysis.confidence_score >= 0.4
                    ? "Средняя точность расчёта"
                    : "Низкая точность — нет аналогов"}
                </p>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="bg-blue-50 rounded-lg p-2">
                    <p className="text-lg font-bold text-blue-800">
                      {(analysis.specialists_count || 0).toLocaleString("ru-RU")}
                    </p>
                    <p className="text-xs text-blue-600">специалистов</p>
                  </div>
                  <div className="bg-purple-50 rounded-lg p-2">
                    <p className="text-lg font-bold text-purple-800">
                      {(analysis.equipment_count || 0).toLocaleString("ru-RU")}
                    </p>
                    <p className="text-xs text-purple-600">ед. техники</p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-2">
                    <p className="text-lg font-bold text-green-800">
                      {(analysis.total_manhours || 0).toLocaleString("ru-RU")}
                    </p>
                    <p className="text-xs text-green-600">чел/часов</p>
                  </div>
                </div>
              </CardBody>
            </Card>
          </div>

          {/* ── AI Reasoning Panel ───────────────────────────────────────── */}
          {analysis.reasoning && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100">
                    <svg className="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900">Методология расчёта</h3>
                </div>
              </CardHeader>
              <CardBody>
                <div className="bg-indigo-50 border-l-4 border-indigo-400 rounded-r-lg p-4">
                  <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-line">
                    {analysis.reasoning}
                  </p>
                </div>
              </CardBody>
            </Card>
          )}

          {/* ── Editable Resource Plan ───────────────────────────────────── */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium text-gray-900">
                  Resource Plan
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
                Task Plan
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

          {/* ── Gantt Timeline ───────────────────────────────────────────── */}
          {editTasks.length > 0 && (
            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-medium text-gray-900">Календарный план</h3>
                  <span className="ml-auto text-sm text-gray-500">
                    Итого:{" "}
                    <span className="font-bold text-gray-900">
                      {editTasks.reduce((s, t) => s + t.duration_days, 0)} дн.
                    </span>
                  </span>
                </div>
              </CardHeader>
              <CardBody>
                <div ref={ganttRef} className="w-full" />
                <p className="text-xs text-gray-400 mt-2 text-center">
                  * Задачи показаны последовательно. Фактический план может быть скорректирован.
                </p>
              </CardBody>
            </Card>
          )}

          {/* ── Accept Section ───────────────────────────────────────────── */}
          <Card>
            <CardBody>
              <div className="flex items-end gap-4">
                <div className="flex-1">
                  <label className="block text-lg font-semibold text-gray-900 mb-2">
                    Название проекта
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-primary-500 focus:border-primary-500"
                    placeholder="Введите название проекта..."
                  />
                </div>
                <Button variant="success" onClick={handleAccept}>
                  Принять
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
