import React, { useState, useCallback, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import TicketPreview from "./components/TicketPreview";
import ProjectSelector from "./components/ProjectSelector";
import Toast from "./components/Toast";
import { generateTickets, syncToADO } from "./services/api";

const STEPS = [
  { label: "Upload", fullLabel: "Upload Documents", icon: "📄" },
  { label: "Generate", fullLabel: "AI Analysis", icon: "🤖" },
  { label: "Board", fullLabel: "Board & Agent", icon: "🚀" },
];

export default function App() {
  const [projectId, setProjectId] = useState("");
  const [activeStep, setActiveStep] = useState(0);
  const [hierarchy, setHierarchy] = useState(() => {
    try { const v = localStorage.getItem("poc_hierarchy"); return v ? JSON.parse(v) : null; } catch { return null; }
  });
  const [generating, setGenerating] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState(null);
  const [uploadCount, setUploadCount] = useState(0);
  const [toast, setToast] = useState({ message: null, variant: "error" });

  // Persist hierarchy to localStorage
  useEffect(() => {
    if (hierarchy) localStorage.setItem("poc_hierarchy", JSON.stringify(hierarchy));
    else localStorage.removeItem("poc_hierarchy");
  }, [hierarchy]);

  // Auto-advance to board if we loaded hierarchy from localStorage
  useEffect(() => {
    if (hierarchy && activeStep === 0) setActiveStep(2);
  }, []);

  const showToast = useCallback((message, variant = "error") => {
    setToast({ message, variant });
  }, []);
  const clearToast = useCallback(() => setToast({ message: null, variant: "error" }), []);

  const handleReset = () => {
    setHierarchy(null);
    setUploadCount(0);
    setSyncResult(null);
    setActiveStep(0);
    localStorage.removeItem("poc_hierarchy");
    showToast("Reset complete — start fresh!", "info");
  };

  const handleUploadSuccess = () => {
    setUploadCount((c) => c + 1);
  };

  const handleGenerate = async () => {
    if (!projectId) {
      showToast("Please select a project first", "warning");
      return;
    }
    setGenerating(true);
    setSyncResult(null);
    try {
      const result = await generateTickets(projectId);
      setHierarchy(result);
      setActiveStep(2);
    } catch (err) {
      showToast(
        err.response?.data?.detail ||
          "Failed to generate tickets. Check your API key and try again."
      );
    }
    setGenerating(false);
  };

  const handleUpdate = (globalIndex, updatedItem) => {
    if (!hierarchy) return;
    const allItems = [
      ...hierarchy.epics,
      ...hierarchy.features,
      ...hierarchy.user_stories,
      ...hierarchy.tasks,
    ];
    allItems[globalIndex] = updatedItem;

    let i = 0;
    const epics = allItems.slice(i, (i += hierarchy.epics.length));
    const features = allItems.slice(i, (i += hierarchy.features.length));
    const user_stories = allItems.slice(i, (i += hierarchy.user_stories.length));
    const tasks = allItems.slice(i);

    setHierarchy({ ...hierarchy, epics, features, user_stories, tasks });
  };

  const handleRemove = (globalIndex) => {
    if (!hierarchy) return;
    const allItems = [
      ...hierarchy.epics,
      ...hierarchy.features,
      ...hierarchy.user_stories,
      ...hierarchy.tasks,
    ];
    allItems.splice(globalIndex, 1);

    const epics = allItems.filter((i) => i.type === "Epic");
    const features = allItems.filter((i) => i.type === "Feature");
    const user_stories = allItems.filter((i) => i.type === "User Story");
    const tasks = allItems.filter((i) => i.type === "Task");

    setHierarchy({ ...hierarchy, epics, features, user_stories, tasks });
  };

  const handleSync = async () => {
    if (!hierarchy) return;
    setSyncing(true);
    try {
      const allItems = [
        ...hierarchy.epics,
        ...hierarchy.features,
        ...hierarchy.user_stories,
        ...hierarchy.tasks,
      ];
      const result = await syncToADO(projectId, allItems);
      setSyncResult(result);
      showToast(`Successfully synced ${result.created} work items to ADO`, "success");
    } catch (err) {
      showToast(
        err.response?.data?.detail ||
          "Failed to sync to ADO. Check your ADO configuration."
      );
    }
    setSyncing(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
          <div className="flex items-center justify-between gap-3">
            {/* Logo */}
            <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
              <div className="relative">
                <div className="bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-xl w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center font-bold text-xs sm:text-sm shadow-lg shadow-blue-200">
                  PO
                </div>
                <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 sm:w-3 sm:h-3 bg-green-400 rounded-full border-2 border-white"></div>
              </div>
              <div className="hidden sm:block">
                <h1 className="text-lg font-bold bg-gradient-to-r from-blue-700 to-indigo-600 bg-clip-text text-transparent">
                  PO Copilot
                </h1>
                <p className="text-[10px] text-slate-400 font-medium tracking-wide uppercase">
                  AI-Powered Product Owner Assistant
                </p>
              </div>
              <h1 className="sm:hidden text-base font-bold bg-gradient-to-r from-blue-700 to-indigo-600 bg-clip-text text-transparent">
                PO Copilot
              </h1>
            </div>

            {/* Team Diamond Badge */}
            <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 bg-gradient-to-r from-sky-50 to-blue-50 border border-blue-200 rounded-full">
              <span className="text-sm">💎</span>
              <span className="text-[10px] font-bold text-blue-700 tracking-wide">TEAM DIAMOND</span>
              <span className="text-[9px] text-blue-400 font-medium">× SKF</span>
              <span className="text-[9px] text-blue-300 font-mono">v0.2</span>
            </div>

            {/* Project Selector */}
            <div className="flex items-center gap-2 sm:gap-3">
              <ProjectSelector value={projectId} onChange={setProjectId} />
              {projectId && (
                <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 border border-blue-200 rounded-full">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                  <span className="text-xs font-medium text-blue-700 max-w-[120px] truncate">{projectId}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Stepper */}
      <div className="max-w-7xl mx-auto w-full px-4 sm:px-6 py-4 sm:py-6">
        <div className="flex items-center">
          {STEPS.map((step, idx) => (
            <React.Fragment key={step.label}>
              <button
                onClick={() => setActiveStep(idx)}
                className={`flex items-center gap-1.5 sm:gap-2.5 px-3 sm:px-5 py-2 sm:py-2.5 rounded-xl text-xs sm:text-sm font-medium transition-all duration-200
                  ${
                    activeStep === idx
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-200 scale-[1.02]"
                      : idx < activeStep
                      ? "bg-white text-green-700 border border-green-200 shadow-sm"
                      : "bg-white/60 text-slate-400 border border-slate-200"
                  }`}
              >
                <span className={`w-6 h-6 sm:w-7 sm:h-7 rounded-lg flex items-center justify-center text-[10px] sm:text-xs font-bold ${
                  activeStep === idx
                    ? "bg-white/20"
                    : idx < activeStep
                    ? "bg-green-100 text-green-600"
                    : "bg-slate-100"
                }`}>
                  {idx < activeStep ? "✓" : step.icon}
                </span>
                <span className="hidden sm:inline">{step.fullLabel}</span>
                <span className="sm:hidden">{step.label}</span>
              </button>
              {idx < STEPS.length - 1 && (
                <div className={`flex-1 h-0.5 mx-1.5 sm:mx-3 rounded-full transition-colors ${
                  idx < activeStep ? "bg-green-300" : "bg-slate-200"
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Toast */}
      <Toast message={toast.message} variant={toast.variant} onClose={clearToast} />

      {/* Content — flex-1 to push footer down */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 pb-8 sm:pb-16">

        {/* Step 1: Upload */}
        {activeStep === 0 && (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-4 sm:px-6 py-3 sm:py-4">
              <h2 className="text-base sm:text-lg font-semibold text-white flex items-center gap-2">
                📄 Upload Project Documents
              </h2>
              <p className="text-blue-100 text-xs sm:text-sm mt-1">
                Upload meeting notes, requirement specs, spreadsheets, or any project documentation.
              </p>
            </div>
            <div className="p-4 sm:p-6">
              <FileUpload projectId={projectId} onUploadSuccess={handleUploadSuccess} />
              {uploadCount > 0 && (
                <div className="mt-4 sm:mt-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pt-4 border-t border-slate-100">
                  <p className="text-sm text-slate-500">
                    <span className="font-semibold text-slate-700">{uploadCount}</span>{" "}
                    document{uploadCount > 1 ? "s" : ""} uploaded and indexed
                  </p>
                  <button
                    onClick={() => setActiveStep(1)}
                    className="w-full sm:w-auto px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl text-sm font-medium hover:shadow-lg hover:shadow-blue-200 transition-all flex items-center justify-center gap-2"
                  >
                    Next: AI Analysis
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Step 2: Generate */}
        {activeStep === 1 && (
          <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 px-4 sm:px-6 py-3 sm:py-4">
              <h2 className="text-base sm:text-lg font-semibold text-white flex items-center gap-2">
                🤖 AI-Powered Ticket Generation
              </h2>
              <p className="text-purple-100 text-xs sm:text-sm mt-1">
                The AI analyzes your documents using RAG and creates a structured ADO hierarchy.
              </p>
            </div>
            <div className="p-4 sm:p-8 text-center">
              <div className="max-w-lg mx-auto">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mb-6 sm:mb-8">
                  {[
                    { icon: "👑", label: "Epics", desc: "High-level themes" },
                    { icon: "⚡", label: "Features", desc: "Capabilities" },
                    { icon: "📖", label: "User Stories", desc: "User needs" },
                    { icon: "✅", label: "Tasks", desc: "Implementation" },
                  ].map((item) => (
                    <div key={item.label} className="bg-slate-50 rounded-xl p-3 sm:p-4 border border-slate-100">
                      <div className="text-xl sm:text-2xl mb-1 sm:mb-2">{item.icon}</div>
                      <div className="text-xs font-bold text-slate-700">{item.label}</div>
                      <div className="text-[10px] text-slate-400 mt-0.5 hidden sm:block">{item.desc}</div>
                    </div>
                  ))}
                </div>

                {generating && (
                  <div className="mb-6 p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                    <div className="flex items-center justify-center gap-3 text-indigo-700">
                      <div className="relative">
                        <div className="w-8 h-8 border-2 border-indigo-200 rounded-full"></div>
                        <div className="absolute top-0 left-0 w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
                      </div>
                      <div className="text-left">
                        <p className="text-sm font-medium">Analyzing documents with AI...</p>
                        <p className="text-xs text-indigo-500">Extracting requirements, mapping to ADO hierarchy</p>
                      </div>
                    </div>
                  </div>
                )}

                <button
                  onClick={handleGenerate}
                  disabled={generating || !projectId}
                  className="w-full sm:w-auto px-8 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-xl text-sm font-semibold hover:shadow-lg hover:shadow-purple-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none transition-all inline-flex items-center justify-center gap-2"
                >
                  {generating ? "Processing..." : "✨ Generate ADO Tickets"}
                </button>

                {!projectId && (
                  <p className="text-xs text-amber-600 mt-3 flex items-center justify-center gap-1">
                    <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Select a project first
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Review & Sync */}
        {activeStep === 2 && (
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 sm:mb-6">
              <div>
                <h2 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center gap-2">
                  🎯 Backlog Board
                </h2>
                <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
                  Manage tickets on the board. Assign AI agents to auto-implement and create PRs.
                </p>
              </div>
              <button
                onClick={() => setActiveStep(1)}
                className="self-start text-sm text-slate-500 hover:text-indigo-600 flex items-center gap-1 transition-colors"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Regenerate
              </button>
              <button
                onClick={handleReset}
                className="self-start text-sm text-red-400 hover:text-red-600 flex items-center gap-1 transition-colors ml-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Reset All
              </button>
            </div>
            <TicketPreview
              hierarchy={hierarchy}
              onUpdate={handleUpdate}
              onRemove={handleRemove}
              onSync={handleSync}
              syncing={syncing}
              showToast={showToast}
            />
          </div>
        )}
      </main>

      {/* Footer — always at bottom */}
      <footer className="mt-auto border-t border-slate-200 bg-white/60 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between text-[10px] sm:text-xs text-slate-400">
          <span>PO Copilot v0.2 — Hackathon 2026</span>
          <span className="hidden sm:flex items-center gap-1.5">
            <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-full text-blue-600 font-semibold">💎 Team Diamond</span>
            <span>•</span>
            <span>SKF Powered</span>
          </span>
          <span className="sm:hidden">💎 v0.2</span>
        </div>
      </footer>
    </div>
  );
}
