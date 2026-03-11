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
        margin: { t: 40, b: 10, l: 10, r: 10 },
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
        title: { text: "Бюджет vs Освоено по проектам", font: { size: 14, color: "#374151" } },
        barmode: "group",
        xaxis: { tickangle: -30, tickfont: { size: 10 } },
        yaxis: { title: "млн ₸" },
        legend: { orientation: "h", y: 1.15 },
        margin: { t: 50, b: 110, l: 60, r: 20 },
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

const ChartsSection: React.FC = () => {
  const [charts, setCharts] = useState<ChartsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    analyticsAPI
      .getCharts()
      .then((res) => setCharts(res.data))
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
      {/* Pie charts row */}
      <div className="grid grid-cols-1 gap-5 lg:grid-cols-2">
        <div className="bg-white rounded-lg shadow p-4">
          <PlotlyPie
            data={charts.projects_by_plant}
            colors={PLANT_COLORS}
            title="Проекты по объектам (завод)"
          />
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <PlotlyPie
            data={charts.projects_by_status}
            colors={STATUS_COLORS}
            title="Проекты по статусу"
          />
        </div>
      </div>

      {/* Bar chart */}
      <div className="bg-white rounded-lg shadow p-4">
        <PlotlyBar data={charts.budget_vs_spent} />
      </div>
    </div>
  );
};

export default ChartsSection;
