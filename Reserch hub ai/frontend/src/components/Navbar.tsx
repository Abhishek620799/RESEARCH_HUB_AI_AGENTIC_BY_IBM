// ResearchHub AI - Navigation Bar Component
// Milestone 4: Activity 4.1
// Responsible: Chetan Galphat

import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate("/login"); };
  return (
    <nav className="bg-blue-700 text-white px-6 py-4 flex justify-between items-center shadow-lg">
      <Link to="/" className="text-xl font-bold">ResearchHub AI</Link>
      <div className="flex gap-4 items-center">
        <Link to="/workspaces" className="hover:text-blue-200">Workspaces</Link>
        <Link to="/search" className="hover:text-blue-200">Search Papers</Link>
        <span className="text-blue-200">{user?.username}</span>
        <button onClick={handleLogout} className="bg-blue-500 hover:bg-blue-400 px-3 py-1 rounded">Logout</button>
      </div>
    </nav>
  );
}
