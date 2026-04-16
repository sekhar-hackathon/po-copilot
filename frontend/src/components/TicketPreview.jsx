import React, { useState, useEffect } from "react";
import { runAgent, getGitHubStatus } from "../services/api";

/* ─── Constants ─── */
const TYPE_TOP = {
  Epic: "border-t-purple-500",
  Feature: "border-t-blue-500",
  "User Story": "border-t-emerald-500",
  Task: "border-t-amber-500",
};
const TYPE_BADGE = {
  Epic: "bg-purple-600",
  Feature: "bg-blue-600",
  "User Story": "bg-emerald-600",
  Task: "bg-amber-500",
};
const TYPE_ICON = { Epic: "👑", Feature: "⚡", "User Story": "📖", Task: "✅" };

const AGENT_STATES = {
  idle: { label: "Assign Agent", color: "bg-violet-50 text-violet-600 hover:bg-violet-100 border-violet-200", icon: "🤖" },
  queued: { label: "Queued", color: "bg-yellow-50 text-yellow-600 border-yellow-200", icon: "⏳" },
  working: { label: "Working...", color: "bg-blue-50 text-blue-600 border-blue-200 animate-pulse", icon: "⚙️" },
  done: { label: "PR Created", color: "bg-green-50 text-green-700 border-green-200", icon: "✅" },
  failed: { label: "Failed", color: "bg-red-50 text-red-600 border-red-200", icon: "❌" },
};

const COLUMNS = [
  { id: "backlog", label: "Backlog", icon: "📋", hdr: "bg-slate-100 text-slate-700", dot: "bg-slate-400" },
  { id: "assigned", label: "Agent Assigned", icon: "🤖", hdr: "bg-violet-100 text-violet-700", dot: "bg-violet-500" },
  { id: "in-progress", label: "Agent Working", icon: "⚙️", hdr: "bg-blue-100 text-blue-700", dot: "bg-blue-500 animate-pulse" },
  { id: "done", label: "Done / PR Created", icon: "✅", hdr: "bg-green-100 text-green-700", dot: "bg-green-500" },
];

/* ─── Work Item Card ─── */
function Card({ item, onEdit, onRemove, onAssignAgent, agentState, onMoveTo, githubConfigured }) {
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({ ...item });
  const st = agentState || "idle";
  const as = AGENT_STATES[st] || AGENT_STATES.idle;
  const canAgent = item.type === "User Story" || item.type === "Task";

  if (editing) {
    return (
      <div className="bg-white rounded-lg border-2 border-blue-300 shadow-lg p-3 space-y-2">
        <input className="w-full border rounded px-2.5 py-1.5 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
          value={editData.title} onChange={(e) => setEditData({ ...editData, title: e.target.value })} />
        <textarea className="w-full border rounded px-2.5 py-1.5 text-xs h-16 focus:ring-2 focus:ring-blue-300 focus:outline-none resize-none"
          value={editData.description} onChange={(e) => setEditData({ ...editData, description: e.target.value })} />
        {canAgent && (
          <input type="number" min="1" max="21" placeholder="SP" className="w-16 border rounded px-2 py-1 text-xs"
            value={editData.story_points || ""} onChange={(e) => setEditData({ ...editData, story_points: parseInt(e.target.value) || null })} />
        )}
        <div className="flex gap-1.5">
          <button onClick={() => { onEdit(editData); setEditing(false); }} className="px-2.5 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">Save</button>
          <button onClick={() => setEditing(false)} className="px-2.5 py-1 border text-xs rounded hover:bg-gray-50">Cancel</button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border border-slate-200 border-t-[3px] ${TYPE_TOP[item.type]} shadow-sm hover:shadow-md transition-all group`}>
      {/* Header */}
      <div className="px-3 pt-2.5 pb-1">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5">
            <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider text-white ${TYPE_BADGE[item.type]}`}>
              {TYPE_ICON[item.type]} {item.type}
            </span>
            {item.story_points != null && (
              <span className="w-5.5 h-5.5 rounded-full bg-slate-100 text-slate-600 text-[10px] font-bold flex items-center justify-center px-1.5 py-0.5">{item.story_points}</span>
            )}
          </div>
          <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <button onClick={() => setEditing(true)} className="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-blue-500 transition-colors" title="Edit">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
            <button onClick={onRemove} className="p-1 rounded hover:bg-red-50 text-slate-400 hover:text-red-500 transition-colors" title="Remove">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        </div>
      </div>

      {/* Body */}
      <div className="px-3 pb-2">
        <h4 className="text-[13px] font-semibold text-slate-900 leading-snug">{item.title}</h4>
        <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-2 leading-relaxed">{item.description}</p>
        {item.parent_title && <p className="text-[10px] text-slate-400 mt-1 truncate">↳ {item.parent_title}</p>}
      </div>

      {/* Tags */}
      {item.tags?.length > 0 && (
        <div className="px-3 pb-1.5 flex gap-1 flex-wrap">
          {item.tags.map((t, i) => <span key={i} className="px-1.5 py-0.5 bg-slate-50 text-slate-500 rounded text-[9px] border border-slate-100">{t}</span>)}
        </div>
      )}

      {/* Agent Status Bar */}
      {canAgent && (
        <div className="mx-3 mb-2 rounded-lg border overflow-hidden">
          <div className={`flex items-center justify-between px-2.5 py-1.5 text-[10px] font-semibold ${as.color}`}>
            <span className="flex items-center gap-1">
              <span>{as.icon}</span>
              <span>{as.label}</span>
              {st === "working" && <span className="ml-1 text-[9px] font-normal opacity-60">generating code...</span>}
            </span>
            {st === "idle" && githubConfigured && (
              <button onClick={onAssignAgent} className="px-2 py-0.5 rounded bg-violet-600 text-white text-[9px] font-bold hover:bg-violet-700 transition-colors">
                START
              </button>
            )}
          </div>
          {/* Progress bar for working state */}
          {st === "working" && (
            <div className="h-1 bg-blue-100">
              <div className="h-full bg-blue-500 rounded-r animate-progress" style={{ width: "60%" }} />
            </div>
          )}
        </div>
      )}

      {/* Footer — PR link + move controls */}
      <div className="px-3 py-1.5 border-t border-slate-100 flex items-center justify-between gap-1">
        <div className="flex gap-1">
          {item._column !== "backlog" && (
            <button onClick={() => onMoveTo("backlog")} className="text-[9px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 hover:bg-slate-200">← Backlog</button>
          )}
        </div>
        <div className="flex items-center gap-1.5">
          {item._pr_url && (
            <a href={item._pr_url} target="_blank" rel="noopener noreferrer"
              className="text-[10px] px-2 py-0.5 rounded bg-green-50 text-green-700 hover:bg-green-100 font-semibold flex items-center gap-1 border border-green-200 transition-colors">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 16 16"><path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z" /></svg>
              PR #{item._pr_number}
            </a>
          )}
          {item._branch && (
            <a href={`https://github.com/${item._gh_owner}/${item._gh_repo}/tree/${item._branch}`} target="_blank" rel="noopener noreferrer"
              className="text-[9px] px-1.5 py-0.5 rounded bg-slate-50 text-slate-500 hover:bg-slate-100 border border-slate-200 truncate max-w-[100px]">
              🌿 {item._branch.replace("agent/", "")}
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

/* ─── Agent Activity Log ─── */
function AgentLog({ entries }) {
  if (entries.length === 0) return null;
  return (
    <div className="bg-slate-900 rounded-xl border border-slate-700 overflow-hidden">
      <div className="px-4 py-2 bg-slate-800 flex items-center gap-2 border-b border-slate-700">
        <div className="flex gap-1">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500" />
          <div className="w-2.5 h-2.5 rounded-full bg-yellow-500" />
          <div className="w-2.5 h-2.5 rounded-full bg-green-500" />
        </div>
        <span className="text-xs text-slate-400 font-mono">Agent Activity Log</span>
      </div>
      <div className="p-3 max-h-48 overflow-y-auto space-y-1 font-mono text-[11px]">
        {entries.map((e, i) => (
          <div key={i} className={`flex items-start gap-2 ${e.type === "error" ? "text-red-400" : e.type === "success" ? "text-green-400" : "text-slate-400"}`}>
            <span className="text-slate-600 flex-shrink-0">{e.time}</span>
            <span className={e.type === "success" ? "text-green-400" : e.type === "error" ? "text-red-400" : e.type === "info" ? "text-blue-400" : "text-slate-300"}>
              {e.message}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── Main Board ─── */
export default function TicketPreview({ hierarchy, onUpdate, onRemove, onSync, syncing, showToast }) {
  const [viewMode, setViewMode] = useState("board");
  const [ticketColumns, setTicketColumns] = useState({});
  const [agentStates, setAgentStates] = useState({}); // key -> idle|queued|working|done|failed
  const [agentLog, setAgentLog] = useState([]);
  const [gh, setGh] = useState(null);

  useEffect(() => {
    getGitHubStatus().then(setGh).catch(() => setGh({ configured: false }));
  }, []);

  if (!hierarchy) return null;

  const allItems = [...hierarchy.epics, ...hierarchy.features, ...hierarchy.user_stories, ...hierarchy.tasks];
  const groups = [
    { label: "Epics", items: hierarchy.epics, type: "Epic" },
    { label: "Features", items: hierarchy.features, type: "Feature" },
    { label: "User Stories", items: hierarchy.user_stories, type: "User Story" },
    { label: "Tasks", items: hierarchy.tasks, type: "Task" },
  ];
  const totalPts = allItems.reduce((s, i) => s + (i.story_points || 0), 0);
  const now = () => new Date().toLocaleTimeString("en-US", { hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" });

  const addLog = (message, type = "info") => {
    setAgentLog((prev) => [...prev, { time: now(), message, type }]);
  };

  const key = (item) => `${item.type}::${item.title}`;

  const enriched = allItems.map((item, idx) => ({
    ...item,
    _gi: idx,
    _column: ticketColumns[key(item)] || "backlog",
    _gh_owner: gh?.owner,
    _gh_repo: gh?.repo,
  }));

  const colItems = (colId) => enriched.filter((i) => i._column === colId);

  const moveTo = (item, col) => setTicketColumns((p) => ({ ...p, [key(item)]: col }));

  // Count items by agent state
  const agentableItems = enriched.filter((i) => i.type === "User Story" || i.type === "Task");
  const donePRs = agentableItems.filter((i) => agentStates[key(i)] === "done");
  const workingCount = agentableItems.filter((i) => agentStates[key(i)] === "working").length;

  const handleAssignAgent = async (item) => {
    if (!gh?.configured) {
      showToast?.("GitHub not configured. Set GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO in .env", "warning");
      return;
    }
    const k = key(item);
    setAgentStates((p) => ({ ...p, [k]: "queued" }));
    moveTo(item, "assigned");
    addLog(`🎯 Agent assigned to: ${item.title}`);

    // Brief delay to show queued state
    await new Promise((r) => setTimeout(r, 500));

    setAgentStates((p) => ({ ...p, [k]: "working" }));
    moveTo(item, "in-progress");
    addLog(`⚙️ Agent started working on: ${item.title}`);
    addLog(`📖 Reading ticket requirements...`);

    try {
      const result = await runAgent({
        type: item.type,
        title: item.title,
        description: item.description,
        acceptance_criteria: item.acceptance_criteria,
        parent_title: item.parent_title,
        tags: item.tags,
      });

      if (result.status === "success") {
        onUpdate(item._gi, {
          ...allItems[item._gi],
          _pr_url: result.pr_url,
          _pr_number: result.pr_number,
          _branch: result.branch,
        });
        setAgentStates((p) => ({ ...p, [k]: "done" }));
        moveTo(item, "done");
        addLog(`✅ PR #${result.pr_number} created → ${result.files_created} files on branch ${result.branch}`, "success");
        addLog(`🔗 ${result.pr_url}`, "success");
        showToast?.(`Agent created PR #${result.pr_number} with ${result.files_created} files`, "success");
      } else {
        setAgentStates((p) => ({ ...p, [k]: "failed" }));
        moveTo(item, "backlog");
        addLog(`❌ Agent failed: ${result.message || "Unknown error"}`, "error");
        showToast?.(result.message || "Agent failed", "error");
      }
    } catch (err) {
      setAgentStates((p) => ({ ...p, [k]: "failed" }));
      moveTo(item, "backlog");
      addLog(`❌ Error: ${err.response?.data?.detail || err.message}`, "error");
      showToast?.(err.response?.data?.detail || "Agent failed", "error");
    }
  };

  const handleAssignAll = async () => {
    const candidates = agentableItems.filter((i) => !agentStates[key(i)] || agentStates[key(i)] === "idle" || agentStates[key(i)] === "failed");
    if (candidates.length === 0) { showToast?.("No tickets to assign", "info"); return; }
    addLog(`🚀 Batch assign: ${candidates.length} tickets to AI agents`);
    for (const item of candidates) {
      await handleAssignAgent(item);
    }
    addLog(`🏁 All agents finished`, "success");
  };

  return (
    <div className="space-y-4">
      {/* ─── Top Bar ─── */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3 p-3 sm:p-4">
          {/* Stats */}
          <div className="flex flex-wrap items-center gap-2 sm:gap-3">
            <div className="bg-slate-50 rounded-xl px-3 py-1.5 border border-slate-100 text-center min-w-[52px]">
              <p className="text-[9px] uppercase tracking-wider text-slate-400 font-medium">Items</p>
              <p className="text-lg font-bold text-slate-800">{allItems.length}</p>
            </div>
            <div className="bg-indigo-50 rounded-xl px-3 py-1.5 border border-indigo-100 text-center min-w-[52px]">
              <p className="text-[9px] uppercase tracking-wider text-indigo-400 font-medium">Points</p>
              <p className="text-lg font-bold text-indigo-700">{totalPts}</p>
            </div>
            <div className="h-7 w-px bg-slate-200 hidden sm:block" />
            {groups.map((g) => g.items.length > 0 && (
              <div key={g.type} className="flex items-center gap-1 px-1.5 py-0.5">
                <span className="text-xs">{TYPE_ICON[g.type]}</span>
                <span className="text-[11px] font-bold text-slate-700">{g.items.length}</span>
              </div>
            ))}
            <div className="h-7 w-px bg-slate-200 hidden sm:block" />
            {/* Agent stats */}
            <div className="flex items-center gap-2">
              {workingCount > 0 && (
                <span className="flex items-center gap-1 px-2 py-1 rounded-lg bg-blue-50 text-blue-700 text-[10px] font-semibold border border-blue-200 animate-pulse">
                  ⚙️ {workingCount} agent{workingCount > 1 ? "s" : ""} working
                </span>
              )}
              {donePRs.length > 0 && (
                <span className="flex items-center gap-1 px-2 py-1 rounded-lg bg-green-50 text-green-700 text-[10px] font-semibold border border-green-200">
                  ✅ {donePRs.length} PR{donePRs.length > 1 ? "s" : ""} created
                </span>
              )}
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center gap-2 flex-shrink-0 flex-wrap">
            {/* GitHub badge */}
            {gh?.configured ? (
              <a href={`https://github.com/${gh.owner}/${gh.repo}`} target="_blank" rel="noopener noreferrer"
                className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[11px] font-medium bg-green-50 text-green-700 border border-green-200 hover:bg-green-100 transition-colors">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" /></svg>
                {gh.owner}/{gh.repo}
              </a>
            ) : (
              <span className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-[11px] bg-slate-50 text-slate-400 border border-slate-200">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" /></svg>
                Not connected
              </span>
            )}

            {/* View Toggle */}
            <div className="flex bg-slate-100 rounded-lg p-0.5">
              <button onClick={() => setViewMode("board")}
                className={`px-2 py-1 text-[11px] font-medium rounded-md transition-all ${viewMode === "board" ? "bg-white text-slate-800 shadow-sm" : "text-slate-500"}`}>📋 Board</button>
              <button onClick={() => setViewMode("list")}
                className={`px-2 py-1 text-[11px] font-medium rounded-md transition-all ${viewMode === "list" ? "bg-white text-slate-800 shadow-sm" : "text-slate-500"}`}>☰ List</button>
            </div>

            {/* Assign All Agents */}
            <button onClick={handleAssignAll} disabled={!gh?.configured || workingCount > 0}
              className="px-3 py-1.5 bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-lg text-[11px] font-semibold hover:shadow-lg hover:shadow-violet-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-1.5">
              🤖 Assign All Agents
            </button>

            {/* Open GitHub */}
            {gh?.configured && (
              <a href={`https://github.com/${gh.owner}/${gh.repo}/pulls`} target="_blank" rel="noopener noreferrer"
                className="px-3 py-1.5 bg-slate-800 text-white rounded-lg text-[11px] font-semibold hover:bg-slate-700 transition-colors flex items-center gap-1.5">
                <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 16 16"><path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z" /></svg>
                View PRs
              </a>
            )}

            {/* ADO — future */}
            <button disabled className="px-3 py-1.5 bg-slate-100 text-slate-400 rounded-lg text-[11px] font-medium cursor-not-allowed flex items-center gap-1.5" title="Coming soon">
              <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M0 8.877L2.247 5.91l8.405-3.416V.022l7.37 5.393L2.966 8.338v8.225L0 15.707zm24-4.45v15.12l-7.381 4.453v-2.547l4.81-3.853.006-10.634z" /></svg>
              ADO
            </button>
          </div>
        </div>
      </div>

      {/* ─── Agent Activity Log ─── */}
      {agentLog.length > 0 && <AgentLog entries={agentLog} />}

      {/* ─── BOARD VIEW ─── */}
      {viewMode === "board" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {COLUMNS.map((col) => {
            const items = colItems(col.id);
            return (
              <div key={col.id} className="flex flex-col bg-slate-50/80 rounded-2xl border border-slate-200 overflow-hidden min-h-[200px]">
                <div className={`px-3 py-2 ${col.hdr} flex items-center justify-between`}>
                  <div className="flex items-center gap-1.5">
                    <div className={`w-2 h-2 rounded-full ${col.dot}`} />
                    <span className="text-xs font-semibold">{col.label}</span>
                  </div>
                  <span className="px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-white/60">{items.length}</span>
                </div>
                <div className="flex-1 p-2 space-y-2 overflow-y-auto max-h-[550px]">
                  {items.length === 0 && (
                    <div className="flex items-center justify-center h-20 text-[11px] text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                      {col.id === "backlog" ? "No items" : col.id === "done" ? "PRs will appear here" : "Agents will move cards here"}
                    </div>
                  )}
                  {items.map((item) => (
                    <Card
                      key={key(item)}
                      item={item}
                      onEdit={(data) => onUpdate(item._gi, data)}
                      onRemove={() => onRemove(item._gi)}
                      onAssignAgent={() => handleAssignAgent(item)}
                      agentState={agentStates[key(item)] || "idle"}
                      onMoveTo={(col) => moveTo(item, col)}
                      githubConfigured={gh?.configured}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ─── LIST VIEW ─── */}
      {viewMode === "list" && (
        <div className="space-y-4">
          {groups.map((group) => group.items.length > 0 && (
            <div key={group.type}>
              <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2 pb-2 border-b border-slate-100">
                <span>{TYPE_ICON[group.type]}</span> {group.label}
                <span className="ml-1 px-2 py-0.5 bg-slate-100 rounded-full text-xs text-slate-500 font-normal">{group.items.length}</span>
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5">
                {group.items.map((item, idx) => {
                  let gi = 0;
                  for (const g of groups) { if (g.type === group.type) { gi += idx; break; } gi += g.items.length; }
                  const e = { ...item, _gi: gi, _column: ticketColumns[key(item)] || "backlog", _gh_owner: gh?.owner, _gh_repo: gh?.repo };
                  return (
                    <Card key={key(e)} item={e}
                      onEdit={(d) => onUpdate(gi, d)} onRemove={() => onRemove(gi)}
                      onAssignAgent={() => handleAssignAgent(e)} agentState={agentStates[key(e)] || "idle"}
                      onMoveTo={(c) => moveTo(e, c)} githubConfigured={gh?.configured} />
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
