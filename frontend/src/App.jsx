import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const tenantId = "anish-test"; 

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF file first!");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("tenant_id", tenantId);

    try {
      setLoading(true);
      await axios.post("http://127.0.0.1:8000/api/upload", formData);
      alert("✅ Document successfully indexed!");
    } catch (err) {
      console.error("Upload Error:", err);
      alert("❌ Connection failed. Check if Backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleChat = async () => {
    if (!question) return;
    const userMsg = { role: "user", text: question };
    const newLog = [...chatLog, userMsg];
    setChatLog(newLog);
    setQuestion("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        question: question,
        tenant_id: tenantId
      });
      setChatLog([...newLog, { role: "ai", text: res.data.answer }]);
    } catch (err) {
      console.error("Chat Error:", err);
      setChatLog([...newLog, { role: "ai", text: "Error: AI not responding." }]);
    }
  };

  return (
    <div style={{ padding: '40px', backgroundColor: '#0f172a', color: 'white', minHeight: '100vh' }}>
      <h1 style={{ color: '#3b82f6' }}>DocuMind RAG Dashboard</h1>
      <p style={{ color: '#94a3b8' }}>Enterprise AI Knowledge Assistant</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '30px', marginTop: '30px' }}>
        <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px' }}>
          <h2>1. Upload</h2>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} style={{ margin: '20px 0' }} />
          <button 
            onClick={handleUpload} 
            disabled={loading}
            style={{ width: '100%', padding: '10px', backgroundColor: '#10b981', color: 'white', border: 'none', borderRadius: '6px' }}
          >
            {loading ? "PROCESSING..." : "INGEST PDF"}
          </button>
        </div>

        <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', height: '500px', display: 'flex', flexDirection: 'column' }}>
          <h2>2. Chat</h2>
          <div style={{ flex: 1, overflowY: 'auto', marginBottom: '20px', background: '#0f172a', padding: '10px', borderRadius: '8px' }}>
            {chatLog.map((m, i) => (
              <p key={i}><strong>{m.role === 'user' ? 'You: ' : 'AI: '}</strong>{m.text}</p>
            ))}
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input value={question} onChange={(e) => setQuestion(e.target.value)} style={{ flex: 1, padding: '10px' }} placeholder="Ask..." />
            <button onClick={handleChat} style={{ padding: '10px 20px', backgroundColor: '#3b82f6', color: 'white', border: 'none' }}>Ask</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;