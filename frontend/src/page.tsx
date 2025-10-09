"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [table, setTable] = useState<string>("skaters");
  const [message, setMessage] = useState<string>("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`http://localhost:8000/data/upload?table=${table}`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setMessage(`Upload success: ${data.records} records added.`);
    } catch (error) {
      setMessage(`Error: ${error}`);
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <h2 className="text-xl mb-4">Upload Data to DB</h2>
      <select
        className="border p-2 mb-2 w-full"
        value={table}
        onChange={(e) => setTable(e.target.value)}
      >
        <option value="skaters">Skaters</option>
        <option value="goalies">Goalies</option>
        <option value="teams">Teams</option>
        <option value="games">Games/Schedule</option>
        {/* Add more tables as we expand */}
      </select>
      <input
        type="file"
        accept=".csv,.xlsx"
        className="border p-2 mb-2 w-full"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <button
        className="bg-blue-600 text-white p-2 rounded"
        onClick={handleUpload}
      >
        Upload
      </button>
      {message && <p className="mt-2 text-green-600">{message}</p>}
    </div>
  );
}