import React, { useState, useEffect, useRef } from "react";
import { listProjects } from "../services/api";

export default function ProjectSelector({ value, onChange }) {
  const [projects, setProjects] = useState([]);
  const [open, setOpen] = useState(false);
  const [adding, setAdding] = useState(false);
  const [newName, setNewName] = useState("");
  const ref = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    listProjects()
      .then((list) => {
        setProjects(list);
        if (list.length > 0 && !value) {
          onChange(list[0]);
        }
      })
      .catch(() => {});
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (ref.current && !ref.current.contains(e.target)) {
        setOpen(false);
        setAdding(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSelect = (id) => {
    onChange(id);
    setOpen(false);
    setAdding(false);
  };

  const handleAdd = () => {
    const trimmed = newName.trim();
    if (!trimmed) return;
    if (!projects.includes(trimmed)) {
      setProjects((prev) => [...prev, trimmed]);
    }
    onChange(trimmed);
    setNewName("");
    setAdding(false);
    setOpen(false);
  };

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 pl-3 pr-2 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm w-56 sm:w-64 hover:bg-white focus:ring-2 focus:ring-blue-400 focus:outline-none transition-all text-left"
      >
        <svg className="w-4 h-4 text-slate-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
        <span className={`flex-1 truncate ${value ? "text-slate-800" : "text-slate-400"}`}>
          {value || "Select Project..."}
        </span>
        <svg className={`w-4 h-4 text-slate-400 transition-transform ${open ? "rotate-180" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="absolute top-full left-0 mt-1 w-64 bg-white border border-slate-200 rounded-xl shadow-xl z-50 overflow-hidden">
          {/* Existing projects */}
          {projects.length > 0 && (
            <div className="max-h-48 overflow-y-auto">
              {projects.map((p) => (
                <button
                  key={p}
                  onClick={() => handleSelect(p)}
                  className={`w-full text-left px-4 py-2.5 text-sm hover:bg-blue-50 flex items-center gap-2 transition-colors ${
                    value === p ? "bg-blue-50 text-blue-700 font-medium" : "text-slate-700"
                  }`}
                >
                  <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                    value === p ? "bg-blue-500" : "bg-slate-300"
                  }`} />
                  <span className="truncate">{p}</span>
                  {value === p && (
                    <svg className="w-4 h-4 text-blue-500 ml-auto flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              ))}
            </div>
          )}
          {projects.length === 0 && !adding && (
            <div className="px-4 py-3 text-xs text-slate-400 text-center">
              No projects yet. Create one below.
            </div>
          )}

          {/* Divider */}
          <div className="border-t border-slate-100" />

          {/* Add new */}
          {adding ? (
            <div className="p-2 flex gap-1.5">
              <input
                ref={inputRef}
                autoFocus
                type="text"
                placeholder="project-name"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAdd()}
                className="flex-1 border border-slate-200 rounded-lg px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-400 focus:outline-none"
              />
              <button
                onClick={handleAdd}
                disabled={!newName.trim()}
                className="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-40 transition-colors"
              >
                Add
              </button>
            </div>
          ) : (
            <button
              onClick={() => setAdding(true)}
              className="w-full text-left px-4 py-2.5 text-sm text-blue-600 hover:bg-blue-50 flex items-center gap-2 font-medium transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
              </svg>
              New Project
            </button>
          )}
        </div>
      )}
    </div>
  );
}
