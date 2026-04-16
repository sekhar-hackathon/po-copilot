import React, { useCallback, useState, useEffect } from "react";
import { uploadDocument, listProjectFiles, deleteProjectFile } from "../services/api";

const FILE_ICONS = {
  pdf: "📕",
  xlsx: "📊",
  xls: "📊",
  csv: "📊",
  md: "📝",
  txt: "📄",
};

function getIcon(filename) {
  const ext = (filename || "").split(".").pop().toLowerCase();
  return FILE_ICONS[ext] || "📄";
}

export default function FileUpload({ projectId, onUploadSuccess }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [files, setFiles] = useState([]);
  const [error, setError] = useState(null);
  const [deleting, setDeleting] = useState(null);

  // Load existing files when project changes
  useEffect(() => {
    if (!projectId) {
      setFiles([]);
      return;
    }
    listProjectFiles(projectId)
      .then((list) => setFiles(list || []))
      .catch(() => setFiles([]));
  }, [projectId]);

  const handleFiles = useCallback(
    async (fileList) => {
      if (!projectId) {
        setError("Please select a project first.");
        return;
      }
      setUploading(true);
      setError(null);

      for (const file of fileList) {
        try {
          const result = await uploadDocument(projectId, file);
          setFiles((prev) => [
            ...prev,
            { file_id: result.file_id, filename: result.filename, chunks_created: result.chunks_created },
          ]);
          onUploadSuccess?.(result);
        } catch (err) {
          setError(err.response?.data?.detail || `Failed to upload ${file.name}`);
        }
      }
      setUploading(false);
    },
    [projectId, onUploadSuccess]
  );

  const handleDelete = async (fileId, filename) => {
    if (!projectId) return;
    setDeleting(fileId);
    try {
      await deleteProjectFile(projectId, fileId);
      setFiles((prev) => prev.filter((f) => f.file_id !== fileId));
    } catch (err) {
      setError(`Failed to delete ${filename}`);
    }
    setDeleting(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleChange = (e) => {
    if (e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files));
    }
  };

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-6 sm:p-8 text-center transition-colors cursor-pointer
          ${dragActive ? "border-blue-500 bg-blue-50" : "border-slate-300 hover:border-slate-400 hover:bg-slate-50"}`}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => document.getElementById("file-input").click()}
      >
        <input
          id="file-input"
          type="file"
          className="hidden"
          multiple
          accept=".pdf,.xlsx,.xls,.txt,.md,.csv"
          onChange={handleChange}
        />
        {uploading ? (
          <div className="flex items-center justify-center gap-2 text-blue-600">
            <div className="relative">
              <div className="w-6 h-6 border-2 border-blue-200 rounded-full"></div>
              <div className="absolute top-0 left-0 w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <span className="text-sm font-medium">Processing document...</span>
          </div>
        ) : (
          <>
            <svg className="mx-auto h-10 w-10 text-slate-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <p className="mt-2 text-sm font-medium text-slate-600">Drop files here, or click to browse</p>
            <p className="mt-1 text-xs text-slate-400">PDF, XLSX, CSV, TXT, MD — up to 20 MB</p>
          </>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-3">
          <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          <span>{error}</span>
          <button onClick={() => setError(null)} className="ml-auto text-red-400 hover:text-red-600">
            <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
          </button>
        </div>
      )}

      {/* File List */}
      {files.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-semibold text-slate-700">
              Indexed Documents
              <span className="ml-1.5 text-xs font-normal text-slate-400">({files.length})</span>
            </h4>
          </div>
          <div className="border border-slate-200 rounded-xl overflow-hidden divide-y divide-slate-100">
            {files.map((f) => (
              <div
                key={f.file_id}
                className="flex items-center gap-3 px-4 py-2.5 bg-white hover:bg-slate-50 transition-colors group"
              >
                <span className="text-lg flex-shrink-0">{getIcon(f.filename)}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-slate-800 truncate">{f.filename}</p>
                  {f.chunks_created && (
                    <p className="text-[10px] text-slate-400">{f.chunks_created} chunks indexed</p>
                  )}
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); handleDelete(f.file_id, f.filename); }}
                  disabled={deleting === f.file_id}
                  className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 transition-all disabled:opacity-50"
                  title={`Remove ${f.filename}`}
                >
                  {deleting === f.file_id ? (
                    <div className="w-4 h-4 border-2 border-red-300 border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
