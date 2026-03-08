// ResearchHub AI - Search Papers Page
// Milestone 4: Activity 4.1 - Frontend Development
// Milestone 3: Activity 3.2 - Paper Search Integration
// Responsible: Chetan Galphat

import { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import { searchPapers, importPaper, getWorkspaces } from "../services/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [selectedWs, setSelectedWs] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState<string | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => { getWorkspaces().then(res => {
    setWorkspaces(res.data); if (res.data.length > 0) setSelectedWs(res.data[0].id);
  }); }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault(); if (!query.trim()) return;
    setLoading(true); setResults([]);
    try { const res = await searchPapers(query, 10); setResults(res.data); }
    catch { setMessage("Search failed. Try again."); }
    setLoading(false);
  };

  const handleImport = async (paper: any) => {
    if (!selectedWs) { setMessage("Select a workspace first"); return; }
    setImporting(paper.arxiv_id);
    try {
      await importPaper({ ...paper, workspace_id: selectedWs });
      setMessage(`"${paper.title.slice(0, 40)}..." imported!`);
    } catch { setMessage("Import failed"); }
    setImporting(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">Search Research Papers</h1>
        {message && <p className="mb-4 text-green-600 bg-green-50 px-4 py-2 rounded-lg text-sm">{message}</p>}
        <div className="bg-white p-5 rounded-xl shadow mb-6">
          <form onSubmit={handleSearch} className="flex gap-3 mb-4">
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search ArXiv papers..."
              className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400" required />
            <button type="submit" disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {loading ? "Searching..." : "Search"}
            </button>
          </form>
          {workspaces.length > 0 && (
            <div className="flex items-center gap-3">
              <label className="text-sm text-gray-600">Import to:</label>
              <select value={selectedWs} onChange={e => setSelectedWs(parseInt(e.target.value))}
                className="border rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400">
                {workspaces.map(ws => <option key={ws.id} value={ws.id}>{ws.name}</option>)}
              </select>
            </div>
          )}
        </div>
        <div className="space-y-4">
          {results.map(paper => (
            <div key={paper.arxiv_id} className="bg-white p-5 rounded-xl shadow">
              <div className="flex justify-between gap-4">
                <div className="flex-1">
                  <a href={paper.url} target="_blank" rel="noopener noreferrer"
                    className="font-semibold text-blue-700 hover:underline">{paper.title}</a>
                  <p className="text-gray-500 text-sm mt-1">{paper.authors}</p>
                  <p className="text-gray-600 text-sm mt-2 line-clamp-3">{paper.abstract}</p>
                  <p className="text-gray-400 text-xs mt-1">{paper.published}</p>
                </div>
                <button onClick={() => handleImport(paper)} disabled={importing === paper.arxiv_id}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 text-sm whitespace-nowrap self-start">
                  {importing === paper.arxiv_id ? "Importing..." : "Import"}
                </button>
              </div>
            </div>
          ))}
          {results.length === 0 && !loading && <p className="text-center text-gray-400 py-8">Enter a query to search ArXiv papers</p>}
        </div>
      </main>
    </div>
  );
}
