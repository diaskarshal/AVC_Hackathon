import React from "react";
import { Card, CardHeader, CardBody } from "./Card";

interface KPIData {
  label: string;
  value: string | number;
  change?: number;
  trend?: "up" | "down" | "neutral";
  format?: "currency" | "percentage" | "number";
}

interface KPIReportsProps {
  title: string;
  kpis: KPIData[];
}

const KPIReports: React.FC<KPIReportsProps> = ({ title, kpis }) => {
  const formatValue = (value: string | number, format?: string) => {
    if (typeof value === "number") {
      if (format === "currency") {
        return new Intl.NumberFormat("en-US", {
          style: "currency",
          currency: "USD",
        }).format(value);
      } else if (format === "percentage") {
        return `${value.toFixed(1)}%`;
      } else {
        return value.toLocaleString();
      }
    }
    return value;
  };

  const getTrendIcon = (trend?: "up" | "down" | "neutral") => {
    if (trend === "up") {
      return (
        <svg
          className="h-5 w-5 text-green-500"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z"
            clipRule="evenodd"
          />
        </svg>
      );
    } else if (trend === "down") {
      return (
        <svg
          className="h-5 w-5 text-red-500"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </svg>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium leading-6 text-gray-900">{title}</h3>
      </CardHeader>
      <CardBody>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {kpis.map((kpi, index) => (
            <div key={index} className="bg-gray-50 p-4 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="text-sm font-medium text-gray-600">
                  {kpi.label}
                </div>
                {kpi.trend && getTrendIcon(kpi.trend)}
              </div>
              <div className="mt-2 flex items-baseline">
                <div className="text-2xl font-semibold text-gray-900">
                  {formatValue(kpi.value, kpi.format)}
                </div>
                {kpi.change !== undefined && (
                  <div
                    className={`ml-2 text-sm ${
                      kpi.change >= 0 ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {kpi.change >= 0 ? "+" : ""}
                    {kpi.change.toFixed(1)}%
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardBody>
    </Card>
  );
};

export default KPIReports;