import React, { useState } from "react";
import { Card, CardHeader, CardBody } from "../components/Card";
import Button from "../components/Button";
import { importAPI } from "../services/API";

const Import: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first");
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    try {
      let response;
      if (
        selectedFile.name.endsWith(".xlsx") ||
        selectedFile.name.endsWith(".xls")
      ) {
        response = await importAPI.uploadExcel(selectedFile);
      } else if (selectedFile.name.endsWith(".csv")) {
        response = await importAPI.uploadCSV(selectedFile);
      } else {
        throw new Error(
          "Invalid file type. Please upload .xlsx, .xls, or .csv files"
        );
      }

      setResult(response.data);
      setSelectedFile(null);
      const fileInput = document.getElementById(
        "file-upload"
      ) as HTMLInputElement;
      if (fileInput) fileInput.value = "";
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to upload file"
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Import Data</h1>
      </div>

      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Upload Excel or CSV File
          </h3>
        </CardHeader>
        <CardBody className="space-y-4">
          <p className="text-sm text-gray-600">
            Import projects(always first), tasks, resources, and budget data from Excel or
            CSV files. The file should contain sheets/columns matching the
            required format.
          </p>

          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
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
                  htmlFor="file-upload"
                  className="cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                >
                  <span>Upload a file</span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    className="sr-only"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileChange}
                  />
                </label>
                <p className="pl-1 text-sm text-gray-600">
                  or drag and drop
                </p>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                XLSX, XLS, or CSV up to 10MB
              </p>
            </div>
          </div>

          {selectedFile && (
            <div className="flex items-center justify-between bg-gray-50 p-4 rounded-md">
              <div className="flex items-center">
                <svg
                  className="h-5 w-5 text-gray-400 mr-2"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-sm text-gray-900">
                  {selectedFile.name}
                </span>
                <span className="ml-2 text-xs text-gray-500">
                  ({(selectedFile.size / 1024).toFixed(2)} KB)
                </span>
              </div>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => {
                  setSelectedFile(null);
                  const fileInput = document.getElementById(
                    "file-upload"
                  ) as HTMLInputElement;
                  if (fileInput) fileInput.value = "";
                }}
              >
                Remove
              </Button>
            </div>
          )}

          <div className="flex justify-end">
            <Button
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
            >
              {uploading ? "Uploading..." : "Upload and Import"}
            </Button>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {result && (
            <div className="bg-green-50 border border-green-400 text-green-700 px-4 py-3 rounded">
              <h4 className="font-semibold mb-2">Import Successful!</h4>
              <div className="text-sm space-y-1">
                {result.stats?.projects !== undefined && (
                  <p>Projects imported: {result.stats.projects}</p>
                )}
                {result.stats?.tasks !== undefined && (
                  <p>Tasks imported: {result.stats.tasks}</p>
                )}
                {result.stats?.resources !== undefined && (
                  <p>Resources imported: {result.stats.resources}</p>
                )}
                {result.stats?.budgets !== undefined && (
                  <p>Budgets imported: {result.stats.budgets}</p>
                )}
              </div>
            </div>
          )}
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Import Format Guide
          </h3>
        </CardHeader>
        <CardBody>
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">
                Excel Format (Multi-sheet)
              </h4>
              <p className="text-sm text-gray-600 mb-2">
                Create separate sheets for each data type:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
              <li>
                <strong>Projects:</strong> name (or project_name), description, status,
                start_date, end_date, total_budget, spent_amount, location
              </li>
              <li>
                <strong>Tasks:</strong> project_id OR project_name, name (or task_name), description,
                status, priority, start_date, end_date, progress,
                assigned_to
              </li>
              <li>
                <strong>Resources:</strong> project_id OR project_name, name (or resource_name),
                resource_type, status, quantity, unit, unit_cost, supplier
              </li>
              <li>
                <strong>Budgets:</strong> project_id OR project_name, category,
                description, planned_amount, actual_amount
              </li>
            </ul>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">
                CSV Format (Single entity type)
              </h4>
              <p className="text-sm text-gray-600">
                CSV files should contain columns matching one of the formats
                above. The system will auto-detect the entity type based on
                the columns.
              </p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};

export default Import;