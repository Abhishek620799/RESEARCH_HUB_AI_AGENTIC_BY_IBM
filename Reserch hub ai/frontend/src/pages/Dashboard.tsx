// ResearchHub AI - Dashboard Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome, {user?.full_name || user?.username}!</h1>
        <p className="text-gray-500 mb-8">ResearchHub AI - Your intelligent research paper assistant</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/workspaces" className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition border border-gray-100">
            <h3 className="text-lg font-semibold text-blue-700 mb-2">My Workspaces</h3>
            <p className="text-gray-500 text-sm">Organize your research papers into project workspaces</p>
          </Link>
          <Link to="/search" className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition border border-gray-100">
            <h3 className="text-lg font-semibold text-green-700 mb-2">Search Papers</h3>
            <p className="text-gray-500 text-sm">Search ArXiv for research papers and import them</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
