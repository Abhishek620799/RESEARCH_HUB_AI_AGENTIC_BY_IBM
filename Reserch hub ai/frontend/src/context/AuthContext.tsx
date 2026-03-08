// ResearchHub AI - Authentication Context
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

interface User { id: number; username: string; email: string; full_name?: string; }
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      axios.get(`${API_URL}/auth/me`)
        .then(res => setUser(res.data))
        .catch(() => { setToken(null); localStorage.removeItem("token"); });
    }
  }, [token]);

  const login = async (username: string, password: string) => {
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);
    const res = await axios.post(`${API_URL}/auth/login`, form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    const newToken = res.data.access_token;
    setToken(newToken);
    localStorage.setItem("token", newToken);
    axios.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;
    const userRes = await axios.get(`${API_URL}/auth/me`);
    setUser(userRes.data);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    delete axios.defaults.headers.common["Authorization"];
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
