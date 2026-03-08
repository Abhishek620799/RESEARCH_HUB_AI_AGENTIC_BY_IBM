// ResearchHub AI - API Service Layer
// Milestone 4: Activity 4.1 - Frontend Services
// Responsible: Chetan Galphat
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/api";

export const api = axios.create({ baseURL: API_URL });

// Interceptor: attach token from localStorage on every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

// Workspaces
export const getWorkspaces = () => api.get("/workspaces/");
export const createWorkspace = (name: string, description?: string) =>
  api.post("/workspaces/", { name, description });
export const deleteWorkspace = (id: number) => api.delete(`/workspaces/${id}`);

// Papers
export const searchPapers = (query: string, max?: number) =>
  api.get("/papers/search", { params: { query, max_results: max || 10 } });
export const importPaper = (paper: object) => api.post("/papers/import", paper);
export const getWorkspacePapers = (workspaceId: number) =>
  api.get(`/papers/workspace/${workspaceId}`);
export const deletePaper = (id: number) => api.delete(`/papers/${id}`);

// Chat
export const sendMessage = (workspace_id: number, message: string) =>
  api.post("/chat/", { workspace_id, message });
export const getChatHistory = (workspaceId: number) =>
  api.get(`/chat/history/${workspaceId}`);
export const clearChatHistory = (workspaceId: number) =>
  api.delete(`/chat/history/${workspaceId}`);
