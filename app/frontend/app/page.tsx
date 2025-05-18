"use client";

import { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";

export default function Home() {
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [graphData, setGraphData] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/upload`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("Upload response:", res.data);
      setUploadResult(res.data);
      
      // Automatically load summary after successful upload
      if (res.data.status === "success") {
        loadSummary();
      }
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
      console.error("Upload error:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadSummary = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/graph/summary`
      );
      console.log("Summary response:", res.data);
      setSummary(res.data);
      
      // Process summary data for chart if available
      if (res.data && res.data.monthly_spending) {
        const chartData = Object.entries(res.data.monthly_spending).map(([month, amount]) => ({
          month,
          amount: parseFloat(amount)
        }));
        setGraphData(chartData);
      }
    } catch (error) {
      setError(error.response?.data?.detail || error.message);
      console.error("Summary error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">AI Finance Tracker</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Upload Financial Document</h2>
        <div className="flex flex-col md:flex-row gap-4 items-center">
          <input
            type="file"
            accept=".csv,.xls,.xlsx,.pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="flex-1 border border-gray-300 rounded p-2"
          />
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded disabled:opacity-50"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? "Processing..." : "Upload & Ingest"}
          </button>
        </div>
        
        {error && (
          <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {error}
          </div>
        )}
      </div>

      {uploadResult && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Upload Result</h2>
          {uploadResult.status === "success" && (
            <div className="mb-4 p-3 bg-green-100 border border-green-400 text-green-700 rounded">
              ✅ Upload successful: {uploadResult.rows_received} rows processed.
            </div>
          )}
          <div className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-60">
            <pre>{JSON.stringify(uploadResult, null, 2)}</pre>
          </div>
          
          <button
            className="mt-4 bg-gray-800 hover:bg-gray-900 text-white font-medium py-2 px-4 rounded disabled:opacity-50"
            onClick={loadSummary}
            disabled={loading}
          >
            {loading ? "Loading..." : "Refresh Financial Summary"}
          </button>
        </div>
      )}

      {summary && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Financial Summary</h2>
          
          {graphData && graphData.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-medium mb-2">Monthly Spending</h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={graphData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value}`, 'Amount']} />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="amount" 
                      stroke="#3B82F6" 
                      name="Spending" 
                      strokeWidth={2}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
          
          <div className="mb-4">
            <h3 className="text-lg font-medium mb-2">Summary Details</h3>
            <div className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-60">
              <pre>{JSON.stringify(summary, null, 2)}</pre>
            </div>
          </div>
          
          {summary.top_categories && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="text-lg font-medium mb-2">Top Categories</h3>
                <ul className="space-y-2">
                  {Object.entries(summary.top_categories).map(([category, amount], index) => (
                    <li key={index} className="flex justify-between">
                      <span>{category}</span>
                      <span className="font-medium">${parseFloat(amount).toFixed(2)}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              {summary.total_info && (
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="text-lg font-medium mb-2">Financial Overview</h3>
                  <ul className="space-y-2">
                    {Object.entries(summary.total_info).map(([key, value], index) => (
                      <li key={index} className="flex justify-between">
                        <span>{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <span className="font-medium">
                          {typeof value === 'number' ? `$${value.toFixed(2)}` : value}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </main>
  );
}