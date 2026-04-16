import React, { useState, useEffect } from "react";
import { runAgent, getGitHubStatus } from "../services/api";

/* ─── Constants ─── */
const TYPE_TOP_BORDER = {
  Epic: "border-t-purple-500",
  Feature: "border-t-blue-500",
  "User Story": "border-t-emerald-500",
  Task: "border-t-amber-500",
};

const TYPE_BADGE = {
  Epic: "bg-purple-600 text-white",
  Feature: "bg-blue-600 text-white",
  "User Story": "bg-emerald-600 text-white",
  Task: "bg-amber-500 text-white",
};

const TYPE_ICONS = {
  Epic: "👑",
  Feature: "⚡",
  "User Story": "📖",
  Task: "✅",
};

const COLUMNS = [
  { id: "todo", label: "To Do", icon: "📋", headerColor: "bg-slate-100 text-slate-700" },
  { id: "in-progress", label: "In Progress", icon: "🔄", headerColor: "bg-blue-100 text-blue-700" },
  { id: "done", label: "Done", icon: "✅", headerColor: "bg-green-100 text-green-700" },
];

/* ─── ADO-Style Work Item Card ─── */
function WorkItemCard({ item, onEdit, onRemove, onStartAgent, agentStatus, onMoveStatus }) {
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({ ...item });
  const status = item._status || "todo";
  const isAgentRunning = agentStatus === "running";

  if (editing) {
    return (
      <div className="bg-white rounded-lg border border-blue-300 shadow-lg p-3 space-y-2 ring-2 ring-blue-100">
        <input
          className="w-full border border-slate-200 rounded px-2.5 py-1.5 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
          value={editData.title}
          onChange={(e) => setEditData({ ...editData, title: e.target.value })}
        />
        <textarea
          className="w-full border rounded px-2.5 py-1.5 text-xs h-16 focus:ring-2 focus:ring-blue-300 focus:outline-none resize-none"
          value={editData.description}
          onChange={(e) => setEditData({ ...editData, description: e.target.value })}
        />
        {(item.type === "User Story" || item.type === "Task") && (
          <input
            type="number" min="1" max="21" placeholder="Story Points"
            className="w-20 border rounded px-2 py-1 text-xs"
            value={editData.story_points || ""}
            onChange={(e) => setEditData({ ...editData, story_points: parseInt(e.target.value) || null })}
          />
        )}
        <div className="flex gap-1.5">
          <button onClick={() => { onEdit(editData); setEditing(false); }} className="px-2.5 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700">Save</button>
          <button onClick={() => setEditing(false)} className="px-2.5 py-1 border text-xs rounded hover:bg-gray-50">Cancel</button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg border border-slate-200 border-t-[3px] ${TYPE_TOP_BORDER[item.type]} shadow-sm hover:shadow-md transition-all group cursor-default`}>
      {/* Card Header */}
      <div className="px-3 pt-2.5 pb-1.5">
        <div className="flex items-center justify-between gap-1.5">
          <div className="flex items-center gap-1.5 min-w-0">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide ${TYPE_BADGE[item.type]}`}>
              {TYPE_ICONS[item.type]} {item.type}
            </span>
            {item.story_points != null && (
              <span className="w-6 h-6 rounded-full bg-slate-100 text-slate-600 text-[10px] font-bold flex items-center justify-center flex-shrink-0">
                {item.story_points}
              </span>
            )}
          </div>
          <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <button onClick={() => setEditing(true)} className="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-blue-500" title="Edit">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
            <button onClick={onRemove} className="p-1 rounded hover:bg-red-50 text-slate-400 hover:text-red-500" title="Remove">
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
            </button>
          </div>
        </div>
      </div>

      {/* Card Body */}
      <div className="px-3 pb-2">
        <h4 className="text-sm font-semibold text-slate-900 leading-snug">{item.title}</h4>
        <p className="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">{item.description}</p>
      </div>

      {/* Parent link */}
      {item.parent_title && (
        <div className="px-3 pb-1.5">
          <p className="text-[10px] text-slate-400 truncate">↳ {item.parent_title}</p>
        </div>
      )}

      {/* Tags */}
      {item.tags?.length > 0 && (
        <div className="px-3 pb-2 flex gap-1 flex-wrap">
          {item.tags.map((tag, i) => (
            <span key={i} className="px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded text-[10px]">{tag}</span>
          ))}
        </div>
      )}

      {/* Card Footer — Agent + Status Controls */}
      <div className="px-3 py-2 border-t border-slate-100 flex items-center justify-between gap-1.5">
        {/* Status move buttons */}
        <div className="flex gap-1">
          {status !== "todo" && (
            <button
              onClick={() => onMoveStatus(status === "done" ? "in-progress" : "todo")}
              className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 hover:bg-slate-200 transition-colors"
              title="Move back"
            >
              ← Back
            </button>
          )}
          {status !== "done" && (
            <button
              onClick={() => onMoveStatus(status === "todo" ? "in-progress" : "done")}
              className="text-[10px] px-1.5 py-0.5 rounded bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors"
              title="Move forward"
            >
              Next →
            </button>
          )}
        </div>

        {/* Agent button */}
        {(item.type === "User Story" || item.type === "Task") && status !== "done" && (
          <button
            onClick={onStartAgent}
            disabled={isAgentRunning}
            className={`text-[10px] px-2 py-1 rounded-md font-medium flex items-center gap-1 transition-all ${
              isAgentRunning
                ? "bg-violet-100 text-violet-500 cursor-wait"
                : item._pr_url
                ? "bg-green-50 text-green-600"
                : "bg-violet-50 text-violet-600 hover:bg-violet-100"
            }`}
            title={item._pr_url ? "PR Created" : "Assign AI Agent"}
          >
            {isAgentRunning ? (
              <>
                <div className="w-3 h-3 border-2 border-violet-300 border-t-violet-600 rounded-full animate-spin" />
                Working...
              </>
            ) : item._pr_url ? (
              <>✓ PR Created</>
            ) : (
              <>🤖 Agent</>
            )}
          </button>
        )}

        {/* PR Link */}
        {item._pr_url && (
          <a
            href={item._pr_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[10px] px-2 py-1 rounded-md bg-green-50 text-green-700 hover:bg-green-100 font-medium flex items-center gap-1 transition-colors"
          >
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 16 16"><path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z" /></svg>
            #{item._pr_number}
          </a>
        )}
      </div>
    </div>
  );
}

/* ─── Main Kanban Preview ─── */
export default function TicketPreview({
  hierarchy,
  onUpdate,
  onRemove,
  onSync,
  syncing,
  showToast,
}) {
  const [viewMode, setViewMode] = useState("board");
  const [ticketStatuses, setTicketStatuses] = useState({});
  const [agentRunning, setAgentRunning] = useState({});
  const [githubStatus, setGithubStatus] = useState(null);

  useEffect(() => {
    getGitHubStatus().then(setGithubStatus).catch(() => setGithubStatus({ configured: false }));
  }, []);

  if (!hierarchy) return null;

  const allItems = [
    ...hierarchy.epics,
    ...hierarchy.features,
    ...hierarchy.user_stories,
    ...hierarchy.tasks,
  ];

  const groups = [
    { label: "Epics", items: hierarchy.epics, type: "Epic" },
    { label: "Features", items: hierarchy.features, type: "Feature" },
    { label: "User Stories", items: hierarchy.user_stories, type: "User Story" },
    { label: "Tasks", items: hierarchy.tasks, type: "Task" },
  ];

  const totalPoints = allItems.reduce((sum, item) => sum + (item.story_points || 0), 0);

  // Add status + index to items
  const enrichedItems = allItems.map((item, idx) => ({
    ...item,
    _gi: idx,
    _status: ticketStatuses[`${item.type}-${item.title}`] || "todo",
  }));

  const getColumn = (colId) => enrichedItems.filter((item) => item._status === colId);

  const moveStatus = (item, newStatus) => {
    const key = `${item.type}-${item.title}`;
    setTicketStatuses((prev) => ({ ...prev, [key]: newStatus }));
  };

  const handleStartAgent = async (item) => {
    if (!githubStatus?.configured) {
      showToast?.("GitHub not configured. Set GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO in .env", "warning");
      return;
    }

    const key = `${item.type}-${item.title}`;
    setAgentRunning((prev) => ({ ...prev, [key]: true }));
    moveStatus(item, "in-progress");

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
        // Update the item with PR info
        const gi = item._gi;
        onUpdate(gi, {
          ...allItems[gi],
          _pr_url: result.pr_url,
          _pr_number: result.pr_number,
          _branch: result.branch,
        });
        moveStatus(item, "done");
        showToast?.(
          `Agent created PR #${result.pr_number} with ${result.files_created} files`,
          "success"
        );
      } else {
        showToast?.(result.message || "Agent could not complete the task", "error");
        moveStatus(item, "todo");
      }
    } catch (err) {
      showToast?.(err.response?.data?.detail || "Agent failed. Check GitHub config.", "error");
      moveStatus(item, "todo");
    }

    setAgentRunning((prev) => ({ ...prev, [key]: false }));
  };

  return (
    <div className="space-y-4">
      {/* Summary Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white border border-slate-200 rounded-2xl p-3 sm:p-4 shadow-sm">
        <div className="flex flex-wrap items-center gap-2 sm:gap-4">
          <div className="bg-slate-50 rounded-xl px-3 py-2 border border-slate-100 text-center">
            <p className="text-[10px] uppercase tracking-wider text-slate-400 font-medium">Total</p>
            <p className="text-lg font-bold text-slate-800">{allItems.length}</p>
          </div>
          <div className="bg-indigo-50 rounded-xl px-3 py-2 border border-indigo-100 text-center">
            <p className="text-[10px] uppercase tracking-wider text-indigo-400 font-medium">Points</p>
            <p className="text-lg font-bold text-indigo-700">{totalPoints}</p>
          </div>
          <div className="h-8 w-px bg-slate-200 hidden sm:block" />
          {groups.map((g) => g.items.length > 0 && (
            <div key={g.type} className="flex items-center gap-1.5 px-2 py-1">
              <span className="text-sm">{TYPE_ICONS[g.type]}</span>
              <span className="text-xs font-bold text-slate-700">{g.items.length}</span>
              <span className="text-[10px] text-slate-400 hidden sm:inline">{g.label}</span>
            </div>
          ))}
          <div className="h-8 w-px bg-slate-200 hidden sm:block" />
          {/* GitHub status */}
          <div className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium ${
            githubStatus?.configured ? "bg-green-50 text-green-700" : "bg-slate-50 text-slate-400"
          }`}>
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" /></svg>
            {githubStatus?.configured ? `${githubStatus.owner}/${githubStatus.repo}` : "Not connected"}
          </div>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          {/* View Toggle */}
          <div className="flex bg-slate-100 rounded-lg p-0.5">
            <button
              onClick={() => setViewMode("board")}
              className={`px-2.5 py-1.5 text-xs font-medium rounded-md transition-all ${viewMode === "board" ? "bg-white text-slate-800 shadow-sm" : "text-slate-500"}`}
            >
              📋 Board
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`px-2.5 py-1.5 text-xs font-medium rounded-md transition-all ${viewMode === "list" ? "bg-white text-slate-800 shadow-sm" : "text-slate-500"}`}
            >
              ☰ List
            </button>
          </div>

          {/* ADO Sync — future capability */}
          <button
            onClick={onSync}
            disabled={true}
            className="px-4 py-2 bg-slate-100 text-slate-400 rounded-xl text-xs font-medium cursor-not-allowed flex items-center gap-1.5"
            title="Azure DevOps sync — coming soon"
          >
            <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M0 8.877L2.247 5.91l8.405-3.416V.022l7.37 5.393L2.966 8.338v8.225L0 15.707zm24-4.45v15.12l-7.381 4.453v-2.547l4.81-3.853.006-10.634z" /></svg>
            ADO (Soon)
          </button>
        </div>
      </div>

      {/* ─── BOARD VIEW (Kanban) ─── */}
      {viewMode === "board" && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 min-h-[400px]">
          {COLUMNS.map((col) => {
            const colItems = getColumn(col.id);
            return (
              <div key={col.id} className="flex flex-col bg-slate-50/80 rounded-2xl border border-slate-200 overflow-hidden">
                {/* Column Header */}
                <div className={`px-4 py-2.5 ${col.headerColor} flex items-center justify-between`}>
                  <div className="flex items-center gap-2">
                    <span className="text-sm">{col.icon}</span>
                    <span className="text-sm font-semibold">{col.label}</span>
                  </div>
                  <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-white/60">
                    {colItems.length}
                  </span>
                </div>

                {/* Column Body */}
                <div className="flex-1 p-2.5 space-y-2.5 overflow-y-auto max-h-[600px]">
                  {colItems.length === 0 && (
                    <div className="flex items-center justify-center h-24 text-xs text-slate-400 border-2 border-dashed border-slate-200 rounded-xl">
                      No items
                    </div>
                  )}
                  {colItems.map((item) => {
                    const key = `${item.type}-${item.title}`;
                    return (
                      <WorkItemCard
                        key={key}
                        item={item}
                        onEdit={(data) => onUpdate(item._gi, data)}
                        onRemove={() => onRemove(item._gi)}
                        onStartAgent={() => handleStartAgent(item)}
                        agentStatus={agentRunning[key] ? "running" : "idle"}
                        onMoveStatus={(newStatus) => moveStatus(item, newStatus)}
                      />
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* ─── LIST VIEW ─── */}
      {viewMode === "list" && (
        <div className="space-y-4">
          {groups.map(
            (group) =>
              group.items.length > 0 && (
                <div key={group.type}>
                  <h3 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2 pb-2 border-b border-slate-100">
                    <span>{TYPE_ICONS[group.type]}</span> {group.label}
                    <span className="ml-1 px-2 py-0.5 bg-slate-100 rounded-full text-xs text-slate-500 font-normal">
                      {group.items.length}
                    </span>
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5">
                    {group.items.map((item, idx) => {
                      let globalIdx = 0;
                      for (const g of groups) {
                        if (g.type === group.type) {
                          globalIdx += idx;
                          break;
                        }
                        globalIdx += g.items.length;
                      }
                      const enriched = {
                        ...item,
                        _gi: globalIdx,
                        _status: ticketStatuses[`${item.type}-${item.title}`] || "todo",
                      };
                      const key = `${item.type}-${item.title}`;
                      return (
                        <WorkItemCard
                          key={key}
                          item={enriched}
                          onEdit={(data) => onUpdate(globalIdx, data)}
                          onRemove={() => onRemove(globalIdx)}
                          onStartAgent={() => handleStartAgent(enriched)}
                          agentStatus={agentRunning[key] ? "running" : "idle"}
                          onMoveStatus={(newStatus) => moveStatus(enriched, newStatus)}
                        />
                      );
                    })}
                  </div>
                </div>
              )
          )}
        </div>
      )}
    </div>
  );
}
