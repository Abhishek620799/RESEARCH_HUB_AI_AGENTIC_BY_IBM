// ResearchHub AI - Register Page
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

export default function RegisterPage() {
  const [form, setForm] = useState({ email: "", username: "", full_name: "", password: "", confirmPassword: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Use relative URL so Vite proxy works in Codespace and localhost both
  const API = "/api";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await axios.post(`${API}/auth/register`, {
        email: form.email,
        username: form.username,
        full_name: form.full_name,
        password: form.password
      });
      navigate("/login");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center text-blue-700 mb-6">ResearchHub AI</h1>
        <h2 className="text-xl font-semibold mb-4 text-center">Create Account</h2>
        {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
        <form onSubmit={handleSubmit} className="space-y-4">
          {["full_name", "username", "email", "password", "confirmPassword"].map(field => (
            <input
              key={field}
              type={field.includes("password") ? "password" : "text"}
              placeholder={field === "confirmPassword" ? "Confirm Password" : field.replace("_", " ").replace(/\b\w/g, c => c.toUpperCase())}
              value={(form as any)[field]}
              onChange={e => setForm({ ...form, [field]: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
              required
            />
          ))}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
        <p className="text-center mt-4 text-sm">
          Have account? <Link to="/login" className="text-blue-600 hover:underline">Sign In</Link>
        </p>
      </div>
    </div>
  );
}
