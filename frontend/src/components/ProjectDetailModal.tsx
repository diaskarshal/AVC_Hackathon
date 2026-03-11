import React, { useEffect, useRef, useState } from "react";
import Modal from "./Modal";
import Button from "./Button";
import {
  Project,
  analyticsAPI,
  tasksAPI,
  resourcesAPI,
  Task,
  Resource,
} from "../services/API";

declare global {
  interface Window {
    Plotly: any;
  }
}

type Tab = "overview" | "tasks" | "resources" | "budget";

interface KPI {
  project_name: string;
  status: string;
  progress: number;
  budget_total: number;
  budget_spent: number;
  budget_remaining: number;
  budget_utilization: number;
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  overdue_tasks: number;
  total_resources: number;
  resource_cost: number;
  start_date: string | null;
  planned_end: string | null;
  actual_end: string | null;
}

interface BudgetBreakdown {
  category: string;
  planned: number;
  actual: number;
  variance: number;
  variance_percentage: number;
}

interface ResourceDistribution {
  [type: string]: { count: number; total_cost: number };
}

const formatKZT = (v: number) =>
  new Intl.NumberFormat("ru-KZ", { maximumFractionDigits: 0 }).format(v) + " ₸";

const formatDate = (s?: string | null) =>
  s ? new Date(s).toLocaleDateString("ru-RU") : "—";

const STATUS_LABEL: Record<string, string> = {
  planning: "Планирование",
  in_progress: "В работе",
  on_hold: "Приостановлен",
  completed: "Завершён",
  cancelled: "Отменён",
};

const STATUS_COLOR: Record<string, string> = {
  planning: "bg-gray-100 text-gray-800",
  in_progress: "bg-blue-100 text-blue-800",
  on_hold: "bg-yellow-100 text-yellow-800",
  completed: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
};

const TASK_STATUS_COLOR: Record<string, string> = {
  not_started: "bg-gray-100 text-gray-700",
  in_progress: "bg-blue-100 text-blue-700",
  completed: "bg-green-100 text-green-700",
  cancelled: "bg-red-100 text-red-700",
};

const RESOURCE_TYPE_COLOR: Record<string, string> = {
  labor: "bg-indigo-100 text-indigo-700",
  equipment: "bg-amber-100 text-amber-700",
  material: "bg-teal-100 text-teal-700",
};

/* ── Plotly donut for budget breakdown ── */
const BudgetPie: React.FC<{ data: BudgetBreakdown[] }> = ({ data }) => {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current || !window.Plotly || data.length === 0) return;
    window.Plotly.newPlot(
      ref.current,
      [
        {
          type: "pie",
          labels: data.map((d) => d.category),
          values: data.map((d) => d.planned),
          hole: 0.4,
          textinfo: "label+percent",
          hovertemplate: "%{label}<br>Плановый: %{value:,.0f} ₸<br>%{percent}<extra></extra>",
          marker: {
            colors: ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#ec4899"],
          },
        },
      ],
      {
        title: { text: "Плановый бюджет по категориям", font: { size: 13 } },
        margin: { t: 40, b: 10, l: 10, r: 10 },
        legend: { orientation: "h", y: -0.2 },
        paper_bgcolor: "rgba(0,0,0,0)",
        height: 260,
      },
      { responsive: true, displayModeBar: false }
    );
    return () => { if (ref.current) window.Plotly.purge(ref.current); };
  }, [data]);
  return <div ref={ref} />;
};

/* ── Resource type bar ── */
const ResourceBar: React.FC<{ data: ResourceDistribution }> = ({ data }) => {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current || !window.Plotly) return;
    const types = Object.keys(data);
    if (types.length === 0) return;
    window.Plotly.newPlot(
      ref.current,
      [
        {
          type: "bar",
          x: types.map((t) => t.charAt(0).toUpperCase() + t.slice(1)),
          y: types.map((t) => data[t].total_cost),
          marker: { color: ["#6366f1", "#f59e0b", "#14b8a6"] },
          hovertemplate: "%{x}<br>%{y:,.0f} ₸<extra></extra>",
        },
      ],
      {
        title: { text: "Стоимость ресурсов по типу", font: { size: 13 } },
        yaxis: { title: "₸", tickformat: ",.0f" },
        margin: { t: 40, b: 50, l: 80, r: 20 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        height: 220,
      },
      { responsive: true, displayModeBar: false }
    );
    return () => { if (ref.current) window.Plotly.purge(ref.current); };
  }, [data]);
  return <div ref={ref} />;
};

/* ════════════════════════════════════════════════════════════ */

interface Props {
  project: Project | null;
  isOpen: boolean;
  onClose: () => void;
  onEdit: (p: Project) => void;
  onDelete: (id: number) => void;
}

const ProjectDetailModal: React.FC<Props> = ({
  project,
  isOpen,
  onClose,
  onEdit,
  onDelete,
}) => {
  const [tab, setTab] = useState<Tab>("overview");
  const [kpi, setKpi] = useState<KPI | null>(null);
  const [budget, setBudget] = useState<BudgetBreakdown[]>([]);
  const [resDist, setResDist] = useState<ResourceDistribution>({});
  const [tasks, setTasks] = useState<Task[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loadingData, setLoadingData] = useState(false);

  const handleExport = () => {
    if (!project) return;
    const lines: string[] = [];

    lines.push("=== ПРОЕКТ ===");
    lines.push(`Название,"${project.name}"`);
    lines.push(`Статус,${project.status}`);
    lines.push(`Объект,"${project.location || "—"}"`);
    if (kpi) {
      lines.push(`Начало,${formatDate(kpi.start_date)}`);
      lines.push(`Плановое завершение,${formatDate(kpi.planned_end)}`);
      lines.push(`Бюджет (₸),${kpi.budget_total}`);
      lines.push(`Освоено (₸),${kpi.budget_spent}`);
      lines.push(`Остаток (₸),${kpi.budget_remaining}`);
      lines.push(`Прогресс (%),${kpi.progress}`);
      lines.push(`Задач всего,${kpi.total_tasks}`);
      lines.push(`Задач завершено,${kpi.completed_tasks}`);
      lines.push(`Просрочено,${kpi.overdue_tasks}`);
    }
    lines.push("");

    if (tasks.length > 0) {
      lines.push("=== ЗАДАЧИ ===");
      lines.push("Задача,Статус,Прогресс %,Ответственный,Дата начала,Плановый срок,Просрочена");
      tasks.forEach((t) => {
        lines.push(
          `"${t.name}",${t.status},${t.progress_percentage},"${t.assigned_to || "—"}",${formatDate(t.start_date)},${formatDate(t.planned_end_date)},${t.is_overdue ? "да" : "нет"}`
        );
      });
      lines.push("");
    }

    if (resources.length > 0) {
      lines.push("=== РЕСУРСЫ ===");
      lines.push("Ресурс,Тип,Количество,Ед. изм.,Ед. стоимость (₸),Итого (₸),Поставщик");
      resources.forEach((r) => {
        lines.push(
          `"${r.name}",${r.resource_type},${r.quantity},"${r.unit || ""}",${r.unit_cost},${r.total_cost},"${r.supplier || "—"}"`
        );
      });
      lines.push("");
    }

    if (budget.length > 0) {
      lines.push("=== БЮДЖЕТ ===");
      lines.push("Категория,Плановый (₸),Фактический (₸),Отклонение (₸),Отклонение (%)");
      budget.forEach((b) => {
        lines.push(
          `"${b.category}",${b.planned},${b.actual},${b.variance},${b.variance_percentage}`
        );
      });
    }

    const csv = "\uFEFF" + lines.join("\n"); // BOM for correct Cyrillic in Excel
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `project_${project.id}_${project.name.replace(/[\s/\\:*?"<>|]/g, "_")}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    if (!project || !isOpen) return;
    setTab("overview");
    setKpi(null);
    setBudget([]);
    setResDist({});
    setTasks([]);
    setResources([]);
    setLoadingData(true);

    Promise.all([
      analyticsAPI.getProjectKPI(project.id),
      analyticsAPI.getBudgetBreakdown(project.id),
      analyticsAPI.getResourceDistribution(project.id),
      tasksAPI.getAll({ project_id: project.id }),
      resourcesAPI.getAll({ project_id: project.id }),
    ])
      .then(([kpiRes, budgetRes, resDistRes, tasksRes, resourcesRes]) => {
        setKpi(kpiRes.data);
        setBudget(budgetRes.data);
        setResDist(resDistRes.data);
        setTasks(tasksRes.data);
        setResources(resourcesRes.data);
      })
      .finally(() => setLoadingData(false));
  }, [project, isOpen]);

  if (!project) return null;

  const tabs: { id: Tab; label: string }[] = [
    { id: "overview", label: "Обзор KPI" },
    { id: "tasks", label: `Задачи (${tasks.length})` },
    { id: "resources", label: `Ресурсы (${resources.length})` },
    { id: "budget", label: "Бюджет" },
  ];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={project.name}
      size="xl"
    >
      <div className="space-y-4">
        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-4" aria-label="Tabs">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`whitespace-nowrap py-2 px-1 border-b-2 text-sm font-medium ${
                  tab === t.id
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                {t.label}
              </button>
            ))}
          </nav>
        </div>

        {loadingData ? (
          <div className="flex items-center justify-center h-48 text-gray-400">
            Загрузка…
          </div>
        ) : (
          <>
            {/* ── OVERVIEW TAB ── */}
            {tab === "overview" && kpi && (
              <div className="space-y-4">
                {/* Header KPI cards */}
                <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
                  <div className="bg-blue-50 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Прогресс</p>
                    <p className="text-2xl font-bold text-blue-600">{kpi.progress}%</p>
                  </div>
                  <div className="bg-green-50 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Бюджет освоен</p>
                    <p className="text-2xl font-bold text-green-600">{kpi.budget_utilization}%</p>
                  </div>
                  <div className="bg-purple-50 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Задач</p>
                    <p className="text-2xl font-bold text-purple-600">{kpi.total_tasks}</p>
                  </div>
                  <div className="bg-orange-50 rounded-lg p-3 text-center">
                    <p className="text-xs text-gray-500">Просрочено</p>
                    <p className="text-2xl font-bold text-orange-600">{kpi.overdue_tasks}</p>
                  </div>
                </div>

                {/* Details grid */}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-500">Статус</p>
                    <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-semibold mt-1 ${STATUS_COLOR[project.status] || "bg-gray-100 text-gray-700"}`}>
                      {STATUS_LABEL[project.status] || project.status}
                    </span>
                  </div>
                  <div>
                    <p className="text-gray-500">Объект</p>
                    <p className="font-medium">{project.location || "—"}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Дата начала</p>
                    <p className="font-medium">{formatDate(kpi.start_date)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Плановое завершение</p>
                    <p className="font-medium">{formatDate(kpi.planned_end)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Бюджет</p>
                    <p className="font-medium">{formatKZT(kpi.budget_total)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Освоено</p>
                    <p className="font-medium">{formatKZT(kpi.budget_spent)}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Ресурсов</p>
                    <p className="font-medium">{kpi.total_resources} ед.</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Стоимость ресурсов</p>
                    <p className="font-medium">{formatKZT(kpi.resource_cost)}</p>
                  </div>
                </div>

                {/* Budget progress bar */}
                <div>
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Освоение бюджета</span>
                    <span>{kpi.budget_utilization}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        kpi.budget_utilization > 90 ? "bg-red-500"
                        : kpi.budget_utilization > 75 ? "bg-yellow-500"
                        : "bg-green-500"
                      }`}
                      style={{ width: `${Math.min(kpi.budget_utilization, 100)}%` }}
                    />
                  </div>
                </div>

                {/* Resource type bar chart */}
                {Object.keys(resDist).length > 0 && (
                  <ResourceBar data={resDist} />
                )}
              </div>
            )}

            {/* ── TASKS TAB ── */}
            {tab === "tasks" && (
              <div className="overflow-y-auto max-h-96">
                {tasks.length === 0 ? (
                  <p className="text-gray-400 text-center py-10">Задачи не найдены</p>
                ) : (
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="text-left text-xs text-gray-500 border-b">
                        <th className="pb-2 pr-4">Задача</th>
                        <th className="pb-2 pr-4">Статус</th>
                        <th className="pb-2 pr-4">Прогресс</th>
                        <th className="pb-2 pr-4">Ответственный</th>
                        <th className="pb-2">Срок</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {tasks.map((t) => (
                        <tr key={t.id} className={t.is_overdue ? "bg-red-50" : ""}>
                          <td className="py-2 pr-4 font-medium text-gray-800 max-w-xs truncate">
                            {t.name}
                          </td>
                          <td className="py-2 pr-4">
                            <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${TASK_STATUS_COLOR[t.status] || "bg-gray-100 text-gray-700"}`}>
                              {t.status.replace("_", " ")}
                            </span>
                          </td>
                          <td className="py-2 pr-4">
                            <div className="flex items-center space-x-1">
                              <div className="w-16 bg-gray-200 rounded-full h-1.5">
                                <div
                                  className="bg-blue-500 h-1.5 rounded-full"
                                  style={{ width: `${t.progress_percentage}%` }}
                                />
                              </div>
                              <span className="text-xs text-gray-500">{t.progress_percentage}%</span>
                            </div>
                          </td>
                          <td className="py-2 pr-4 text-gray-600">{t.assigned_to || "—"}</td>
                          <td className="py-2 text-gray-500">{formatDate(t.planned_end_date)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}

            {/* ── RESOURCES TAB ── */}
            {tab === "resources" && (
              <div className="overflow-y-auto max-h-96">
                {resources.length === 0 ? (
                  <p className="text-gray-400 text-center py-10">Ресурсы не найдены</p>
                ) : (
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="text-left text-xs text-gray-500 border-b">
                        <th className="pb-2 pr-4">Ресурс</th>
                        <th className="pb-2 pr-4">Тип</th>
                        <th className="pb-2 pr-4">Кол-во</th>
                        <th className="pb-2 pr-4">Ед. стоимость</th>
                        <th className="pb-2">Итого</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {resources.map((r) => (
                        <tr key={r.id}>
                          <td className="py-2 pr-4 font-medium text-gray-800">{r.name}</td>
                          <td className="py-2 pr-4">
                            <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${RESOURCE_TYPE_COLOR[r.resource_type] || "bg-gray-100 text-gray-700"}`}>
                              {r.resource_type}
                            </span>
                          </td>
                          <td className="py-2 pr-4">{r.quantity} {r.unit || ""}</td>
                          <td className="py-2 pr-4 text-gray-600">{formatKZT(r.unit_cost)}</td>
                          <td className="py-2 font-semibold">{formatKZT(r.total_cost)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}

            {/* ── BUDGET TAB ── */}
            {tab === "budget" && (
              <div className="space-y-4">
                {budget.length === 0 ? (
                  <p className="text-gray-400 text-center py-10">Данные бюджета не найдены</p>
                ) : (
                  <>
                    <BudgetPie data={budget} />
                    <table className="min-w-full text-sm">
                      <thead>
                        <tr className="text-left text-xs text-gray-500 border-b">
                          <th className="pb-2 pr-4">Категория</th>
                          <th className="pb-2 pr-4 text-right">Плановый</th>
                          <th className="pb-2 pr-4 text-right">Фактический</th>
                          <th className="pb-2 text-right">Отклонение</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100">
                        {budget.map((b) => (
                          <tr key={b.category}>
                            <td className="py-2 pr-4 font-medium">{b.category}</td>
                            <td className="py-2 pr-4 text-right">{formatKZT(b.planned)}</td>
                            <td className="py-2 pr-4 text-right">{formatKZT(b.actual)}</td>
                            <td className={`py-2 text-right font-medium ${b.variance < 0 ? "text-red-600" : "text-green-600"}`}>
                              {b.variance >= 0 ? "+" : ""}
                              {formatKZT(b.variance)}
                              <span className="text-xs ml-1">({b.variance_percentage.toFixed(1)}%)</span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </>
                )}
              </div>
            )}
          </>
        )}

        {/* Action buttons */}
        <div className="flex justify-between items-center pt-4 border-t">
          <Button variant="secondary" onClick={handleExport}>
            ↓ Экспорт CSV
          </Button>
          <div className="flex space-x-3">
            <Button variant="secondary" onClick={onClose}>Закрыть</Button>
            <Button variant="primary" onClick={() => onEdit(project)}>Редактировать</Button>
            <Button variant="danger" onClick={() => onDelete(project.id)}>Удалить</Button>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default ProjectDetailModal;
