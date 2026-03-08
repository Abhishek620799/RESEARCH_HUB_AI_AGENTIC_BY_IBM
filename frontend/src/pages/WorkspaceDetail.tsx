// ResearchHub AI - Workspace Detail with AI Chat
// Milestone 4: Activity 4.1 - Frontend Development
// Milestone 5: Research Paper Analysis UI
// Responsible: Chetan Galphat
import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import { getWorkspacePapers, deletePaper, sendMessage, getChatHistory } from "../services/api";

export default function WorkspaceDetail() {
  const { id } = useParams<{ id: string }>();
  const workspaceId = parseInt(id!);
  const [papers, setPapers] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  const fetchData = async () => {
    try {
      const [papersRes, chatRes] = await Promise.all([
        getWorkspacePapers(workspaceId),
        getChatHistory(workspaceId)
      ]);
      setPapers(papersRes.data);
      setMessages(chatRes.data);
    } catch (err) {
      console.error("Failed to fetch workspace data", err);
    }
  };

  useEffect(() => { fetchData(); }, [workspaceId]);
  useEffect(() => { chatRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = input;
    setInput("");
    setLoading(true);
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    try {
      const res = await sendMessage(workspaceId, userMsg);
      setMessages(prev => [...prev, { role: "assistant", content: res.data.answer }]);
    } catch (err: any) {
      const errMsg = err?.response?.data?.detail || "Error getting response. Please check if the Groq API key is configured.";
      setMessages(prev => [...prev, { role: "assistant", content: errMsg }]);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePaper = async (paperId: number) => {
    if (!confirm("Remove this paper?")) return;
    try {
      await deletePaper(paperId);
      fetchData();
    } catch (err) {
      console.error("Failed to delete paper", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-bold mb-4 text-gray-800">Papers ({papers.length})</h2>
          <div className="space-y-3 max-h-[70vh] overflow-y-auto">
            {papers.map(p => (
              <div key={p.id} className="bg-white p-4 rounded-lg shadow">
                <div className="flex justify-between">
                  <a href={p.url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-700 hover:underline text-sm">{p.title}</a>
                  <button onClick={() => handleDeletePaper(p.id)} className="text-red-400 hover:text-red-600 text-xs ml-2">Remove</button>
                </div>
                <p className="text-gray-500 text-xs mt-1">{p.authors}</p>
              </div>
            ))}
            {papers.length === 0 && <p className="text-gray-400 text-center py-6">No papers yet. Import from Search.</p>}
          </div>
        </div>
        <div className="flex flex-col">
          <h2 className="text-xl font-bold mb-4 text-gray-800">AI Research Assistant</h2>
          <div className="bg-white rounded-xl shadow flex-1 flex flex-col" style={{minHeight: "400px"}}>
            <div className="flex-1 p-4 overflow-y-auto space-y-3 max-h-96">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-xs lg:max-w-sm px-4 py-2 rounded-2xl text-sm ${m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-800"}`}>
                    {m.content}
                  </div>
                </div>
              ))}
              {loading && <div className="flex justify-start"><div className="bg-gray-100 px-4 py-2 rounded-2xl text-sm text-gray-500">Thinking...</div></div>}
              <div ref={chatRef} />
            </div>
            <form onSubmit={handleChat} className="p-4 border-t flex gap-2">
              <input value={input} onChange={e => setInput(e.target.value)} placeholder="Ask about your papers..."
                className="flex-1 border rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400" />
              <button type="submit" disabled={loading || !input.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm hover:bg-blue-700 disabled:opacity-50">Send</button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
