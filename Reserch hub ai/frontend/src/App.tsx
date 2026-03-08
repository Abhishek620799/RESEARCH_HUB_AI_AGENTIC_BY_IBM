// ResearchHub AI - Main App Component with Routing
// Milestone 4: Activity 4.1 - Frontend Development
// Responsible: Chetan Galphat

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Dashboard from "./pages/Dashboard";
import WorkspaceList from "./pages/WorkspaceList";
import WorkspaceDetail from "./pages/WorkspaceDetail";
import SearchPage from "./pages/SearchPage";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/workspaces" element={<PrivateRoute><WorkspaceList /></PrivateRoute>} />
          <Route path="/workspaces/:id" element={<PrivateRoute><WorkspaceDetail /></PrivateRoute>} />
          <Route path="/search" element={<PrivateRoute><SearchPage /></PrivateRoute>} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
