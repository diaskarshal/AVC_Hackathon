import React, { useEffect, useRef, useState } from "react";
import { analyticsAPI } from "../../services/API";

declare global {
  interface Window {
    Plotly: any;
  }
}

interface ChartItem {
  label: string;
  value: number;
}

interface BudgetItem {
  name: string;
  budget: number;
  spent: number;
}

interface ChartsData {
  projects_by_plant: ChartItem[];
  projects_by_status: ChartItem[];
  budget_vs_spent: BudgetItem[];
}

const PLANT_COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"];
const STATUS_COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#6b7280"];

const PlotlyPie: React.FC<{
  data: ChartItem[];
  colors: string[];
  title: string;
}> = ({ data, colors, title }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || !window.Plotly || data.length === 0) return;

    window.Plotly.newPlot(
      ref.current,
      [
        {
          type: "pie",
          labels: data.map((d) => d.label),
          values: data.map((d) => d.value),
          marker: { colors: colors.slice(0, data.length) },
          textinfo: "label+percent",
          hovertemplate: "%{label}: %{value}<br>%{percent}<extra></extra>",
          hole: 0.35,
        },
      ],
      {
        title: { text: title, font: { size: 14, color: "#374151" } },
        margin: { t: 10, b: 10, l: 10, r: 10 },
        showlegend: true,
        legend: { orientation: "h", y: -0.15 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        height: 280,
      },
      { responsive: true, displayModeBar: false }
    );

    return () => {
      if (ref.current) window.Plotly.purge(ref.current);
    };
  }, [data, colors, title]);

  return <div ref={ref} />;
};

const PlotlyBar: React.FC<{ data: BudgetItem[] }> = ({ data }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || !window.Plotly || data.length === 0) return;

    const names = data.map((d) => d.name);

    window.Plotly.newPlot(
      ref.current,
      [
        {
          type: "bar",
          name: "Бюджет (млн ₸)",
          x: names,
          y: data.map((d) => d.budget),
          marker: { color: "#3b82f6" },
          hovertemplate: "%{x}<br>Бюджет: %{y}M ₸<extra></extra>",
        },
        {
          type: "bar",
          name: "Освоено (млн ₸)",
          x: names,
          y: data.map((d) => d.spent),
          marker: { color: "#10b981" },
          hovertemplate: "%{x}<br>Освоено: %{y}M ₸<extra></extra>",
        },
      ],
      {
        title: false,
        barmode: "group",
        xaxis: { tickangle: -30, tickfont: { size: 10 } },
        yaxis: { title: "млн ₸" },
        legend: { orientation: "h", y: 1.15 },
        margin: { t: 10, b: 110, l: 60, r: 20 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        height: 340,
      },
      { responsive: true, displayModeBar: false }
    );

    return () => {
      if (ref.current) window.Plotly.purge(ref.current);
    };
  }, [data]);

  return <div ref={ref} />;
};

interface WorkforceData {
  total_capacity: number;
  total_deployed: number;
  available: number;
  utilization_pct: number;
  active_projects_count: number;
  by_project: { project: string; workers: number; budget: number }[];
}

const WorkforceChart: React.FC<{ data: WorkforceData }> = ({ data }) => {
  const barRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!barRef.current || !window.Plotly) return;

    const { total_capacity, total_deployed, available, by_project } = data;

    // Capacity overview: horizontal stacked bar (deployed + available = total)
    window.Plotly.newPlot(
      barRef.current,
      [
        {
          type: "bar",
          orientation: "h",
          name: "Задействовано",
          x: [total_deployed],
          y: ["Общий штат"],
          marker: { color: "#3b82f6" },
          text: [`${total_deployed} чел.`],
          textposition: "inside",
          hovertemplate: "Задействовано: %{x} чел.<extra></extra>",
        },
        {
          type: "bar",
          orientation: "h",
          name: "Свободно",
          x: [available],
          y: ["Общий штат"],
          marker: { color: "#d1fae5" },
          text: [`${available} свободно`],
          textposition: "inside",
          hovertemplate: "Свободно: %{x} чел.<extra></extra>",
        },
        // Per-project breakdown
        ...by_project.map((p, i) => ({
          type: "bar",
          orientation: "h",
          name: p.project,
          x: [p.workers],
          y: [p.project],
          marker: { color: ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#ede9fe"][i % 6] },
          text: [p.workers > 0 ? `${p.workers}` : ""],
          textposition: "inside",
          hovertemplate: `${p.project}<br>Специалистов: %{x}<extra></extra>`,
          showlegend: false,
        })),
      ],
      {
        barmode: "stack",
        xaxis: { title: "Количество специалистов", range: [0, Math.max(total_capacity, total_deployed) * 1.1] },
        yaxis: { autorange: "reversed", tickfont: { size: 11 }, tickpad: 12 },
        legend: { orientation: "h", y: 1.12 },
        margin: { t: 30, b: 50, l: 180, r: 30 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "#fafafa",
        height: Math.max(220, (by_project.length + 1) * 44 + 100),
        annotations: [
          {
            x: total_capacity,
            y: "Общий штат",
            text: `Штат: ${total_capacity}`,
            showarrow: true,
            arrowhead: 2,
            ax: 40,
            ay: 0,
            font: { size: 11, color: "#374151" },
            bgcolor: "white",
            bordercolor: "#9ca3af",
            borderwidth: 1,
          },
        ],
        shapes: [
          {
            type: "line",
            x0: total_capacity,
            x1: total_capacity,
            y0: -0.5,
            y1: by_project.length + 0.5,
            xref: "x",
            yref: "y",
            line: { color: "#ef4444", dash: "dash", width: 2 },
          },
        ],
      },
      { responsive: true, displayModeBar: false }
    );

    return () => {
      if (barRef.current) window.Plotly.purge(barRef.current);
    };
  }, [data]);

  return (
    <div>
      {/* KPI tiles */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        <div className="bg-blue-50 rounded-lg p-3 text-center">
          <p className="text-2xl font-black text-blue-700">{data.total_capacity.toLocaleString("ru-RU")}+</p>
          <p className="text-xs text-blue-500 mt-0.5">Штатная численность</p>
        </div>
        <div className="bg-indigo-50 rounded-lg p-3 text-center">
          <p className="text-2xl font-black text-indigo-700">{data.total_deployed.toLocaleString("ru-RU")}</p>
          <p className="text-xs text-indigo-500 mt-0.5">Задействовано</p>
        </div>
        <div className="bg-green-50 rounded-lg p-3 text-center">
          <p className="text-2xl font-black text-green-700">{data.available.toLocaleString("ru-RU")}</p>
          <p className="text-xs text-green-500 mt-0.5">Свободно</p>
        </div>
        <div className={`rounded-lg p-3 text-center ${data.utilization_pct >= 80 ? "bg-red-50" : data.utilization_pct >= 50 ? "bg-amber-50" : "bg-gray-50"}`}>
          <p className={`text-2xl font-black ${data.utilization_pct >= 80 ? "text-red-700" : data.utilization_pct >= 50 ? "text-amber-700" : "text-gray-700"}`}>
            {data.utilization_pct}%
          </p>
          <p className={`text-xs mt-0.5 ${data.utilization_pct >= 80 ? "text-red-500" : data.utilization_pct >= 50 ? "text-amber-500" : "text-gray-500"}`}>
            Загрузка персонала
          </p>
        </div>
      </div>
      <div ref={barRef} />
    </div>
  );
};

interface TrendData {
  months: string[];
  planned: number[];
  actual: number[];
  forecast_months: string[];
  forecast: number[];
}

const BudgetTrendLine: React.FC<{ data: TrendData }> = ({ data }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current || !window.Plotly) return;
    if (data.months.length === 0) return;

    // Format months for display: "2024-03" → "Mar '24"
    const fmtMonth = (ym: string) => {
      const [y, m] = ym.split("-");
      return new Date(Number(y), Number(m) - 1).toLocaleDateString("ru-RU", { month: "short", year: "2-digit" });
    };

    const xActual = data.months.map(fmtMonth);
    const xForecast = [xActual[xActual.length - 1], ...data.forecast_months.map(fmtMonth)];
    const yForecast = [data.actual[data.actual.length - 1], ...data.forecast];

    window.Plotly.newPlot(
      ref.current,
      [
        {
          type: "scatter",
          mode: "lines+markers",
          name: "Плановый бюджет",
          x: xActual,
          y: data.planned,
          line: { color: "#3b82f6", width: 2.5, dash: "dot" },
          marker: { color: "#3b82f6", size: 5 },
          hovertemplate: "%{x}<br>План: %{y}M ₸<extra></extra>",
        },
        {
          type: "scatter",
          mode: "lines+markers",
          name: "Фактическое освоение",
          x: xActual,
          y: data.actual,
          line: { color: "#10b981", width: 3 },
          marker: { color: "#10b981", size: 6 },
          hovertemplate: "%{x}<br>Факт: %{y}M ₸<extra></extra>",
        },
        {
          type: "scatter",
          mode: "lines+markers",
          name: "Прогноз",
          x: xForecast,
          y: yForecast,
          line: { color: "#f59e0b", width: 2, dash: "dash" },
          marker: { color: "#f59e0b", size: 5, symbol: "diamond" },
          hovertemplate: "%{x}<br>Прогноз: %{y}M ₸<extra></extra>",
        },
      ],
      {
        title: false,
        xaxis: { showgrid: true, gridcolor: "#f3f4f6" },
        yaxis: { title: "млн ₸", showgrid: true, gridcolor: "#f3f4f6" },
        legend: { orientation: "h", y: 1.18 },
        margin: { t: 10, b: 50, l: 65, r: 20 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "#fafafa",
        height: 320,
        shapes: [
          {
            type: "line",
            x0: xActual[xActual.length - 1],
            x1: xActual[xActual.length - 1],
            y0: 0,
            y1: 1,
            xref: "x",
            yref: "paper",
            line: { color: "#9ca3af", dash: "dot", width: 1 },
          },
        ],
        annotations: [
          {
            x: xActual[xActual.length - 1],
            y: 1,
            xref: "x",
            yref: "paper",
            text: "Сегодня",
            showarrow: false,
            font: { size: 10, color: "#6b7280" },
            yanchor: "bottom",
          },
        ],
      },
      { responsive: true, displayModeBar: false }
    );

    return () => {
      if (ref.current) window.Plotly.purge(ref.current);
    };
  }, [data]);

  return <div ref={ref} />;
};

const ChartsSection: React.FC = () => {
  const [charts, setCharts] = useState<ChartsData | null>(null);
  const [trend, setTrend] = useState<TrendData | null>(null);
  const [workforce, setWorkforce] = useState<WorkforceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      analyticsAPI.getCharts(),
      analyticsAPI.getBudgetTrend(),
      analyticsAPI.getWorkforceUtilization(),
    ])
      .then(([chartsRes, trendRes, workRes]) => {
        setCharts(chartsRes.data);
        setTrend(trendRes.data);
        setWorkforce(workRes.data);
      })
      .catch(() => setError("Не удалось загрузить данные графиков"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-40 text-gray-400">
        Загрузка графиков…
      </div>
    );
  }

  if (error || !charts) {
    return (
      <div className="text-center text-red-500 py-8">{error ?? "Нет данных"}</div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Workforce utilization — top of dashboard, proves resource planning value */}
      {workforce && (
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Загрузка персонала AVC GROUP</h3>
          <WorkforceChart data={workforce} />
        </div>
      )}

      {/* Budget trend line — full width */}
      {trend && trend.months.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">Динамика бюджета</h3>
          <BudgetTrendLine data={trend} />
        </div>
      )}

      {/* Pie charts row */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">Проекты по объектам</h3>
          <PlotlyPie
            data={charts.projects_by_plant}
            colors={PLANT_COLORS}
            title=""
          />
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">Проекты по статусу</h3>
          <PlotlyPie
            data={charts.projects_by_status}
            colors={STATUS_COLORS}
            title=""
          />
        </div>
      </div>

      {/* Bar chart */}
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">Бюджет vs Освоено</h3>
        <PlotlyBar data={charts.budget_vs_spent} />
      </div>
    </div>
  );
};

export default ChartsSection;
