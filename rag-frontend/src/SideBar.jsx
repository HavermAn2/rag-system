
import { useRef, useState } from "react";
import "./SideBar.css";

const initialDocuments = [
  { id: 1, name: "Python Basics.pdf", status: "ready" },
  { id: 2, name: "FastAPI Guide.pdf", status: "ready" },
  { id: 3, name: "Machine Learning.pdf", status: "processing" },
];

export default function Sidebar() {
  const [documents, setDocuments] = useState(initialDocuments);
  const [selectedId, setSelectedId] = useState(1);
  const fileInputRef = useRef(null);

  function handleUpload(event) {
    const files = Array.from(event.target.files || []);

    const newDocuments = files
      .filter((file) => file.name.toLowerCase().endsWith(".pdf"))
      .map((file) => ({
        id: crypto.randomUUID(),
        name: file.name,
        status: "processing",
      }));

    setDocuments((prev) => [...prev, ...newDocuments]);

    // Здесь позже подключим POST /api/v1/documents
    event.target.value = "";
  }

  function handleDelete(id) {
    setDocuments((prev) => prev.filter((doc) => doc.id !== id));

    if (selectedId === id) {
      setSelectedId(null);
    }

    // Здесь позже подключим DELETE /api/v1/documents/{id}
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">✦</div>

        <div>
          <h2>RAG Assistant</h2>
          <span>Document intelligence</span>
        </div>
      </div>

      <div className="sidebar-content">
        <div className="sidebar-section-title">
          <span>YOUR DOCUMENTS</span>
          <span className="document-count">{documents.length}</span>
        </div>

        <button
          className="upload-button"
          onClick={() => fileInputRef.current?.click()}
        >
          <span className="upload-plus">+</span>
          Upload PDF
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          hidden
          onChange={handleUpload}
        />

        <div className="document-list">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className={`document-item ${
                selectedId === doc.id ? "selected" : ""
              }`}
            >
              <button
                className="document-select"
                onClick={() => setSelectedId(doc.id)}
              >
                <span className="file-icon">▤</span>

                <span className="document-info">
                  <span className="document-name" title={doc.name}>
                    {doc.name}
                  </span>

                  <span className={`document-status ${doc.status}`}>
                    <span className="status-dot" />
                    {doc.status === "ready" ? "Ready" : "Processing"}
                  </span>
                </span>
              </button>

              <button
                className="delete-button"
                title="Delete document"
                aria-label={`Delete ${doc.name}`}
                onClick={() => handleDelete(doc.id)}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </div>

      
    </aside>
  );
}
