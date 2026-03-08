// ResearchHub AI - Workspace List Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getWorkspaces, createWorkspace, deleteWorkspace } from "../services/api";

export default function WorkspaceList() {
  const [workspaces, setWorkspaces] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchWorkspaces = async () => {
    try {
      const res = await getWorkspaces();
      setWorkspaces(res.data);
    } catch (err) {
      console.error("Failed to fetch workspaces", err);
    }
  };

  useEffect(() => { fetchWorkspaces(); }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    setError("");
    try {
      await createWorkspace(name, desc);
      setName("");
      setDesc("");
      await fetchWorkspaces();
    } catch (err: any) {
      console.error("Failed to create workspace", err);
      setError(err?.response?.data?.detail || "Failed to create workspace. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this workspace?")) return;
    try {
      await deleteWorkspace(id);
      fetchWorkspaces();
    } catch (err) {
      console.error("Failed to delete workspace", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">My Workspaces</h1>
        <form onSubmit={handleCreate} className="bg-white p-5 rounded-xl shadow mb-8 flex gap-3 flex-wrap">
          <input placeholder="Workspace name" value={name} onChange={e => setName(e.target.value)}
            className="border rounded-lg px-3 py-2 flex-1 min-w-40 focus:ring-2 focus:ring-blue-400 focus:outline-none" required />
          <input placeholder="Description (optional)" value={desc} onChange={e => setDesc(e.target.value)}
            className="border rounded-lg px-3 py-2 flex-1 min-w-40 focus:ring-2 focus:ring-blue-400 focus:outline-none" />
          <button type="submit" disabled={loading}
            className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50">
            {loading ? "Creating..." : "Create"}
          </button>
        </form>
        {error && <p className="text-red-500 mb-4 text-sm">{error}</p>}
        <div className="grid gap-4">
          {workspaces.map(ws => (
            <div key={ws.id} className="bg-white p-5 rounded-xl shadow flex justify-between items-center">
              <div>
                <Link to={`/workspaces/${ws.id}`} className="font-semibold text-blue-700 hover:underline">{ws.name}</Link>
                {ws.description && <p className="text-gray-500 text-sm mt-1">{ws.description}</p>}
              </div>
              <button onClick={() => handleDelete(ws.id)} className="text-red-500 hover:text-red-700 text-sm">Delete</button>
            </div>
          ))}
          {workspaces.length === 0 && <p className="text-gray-500 text-center py-8">No workspaces yet. Create your first one above!</p>}
        </div>
      </main>
    </div>
  );
}
