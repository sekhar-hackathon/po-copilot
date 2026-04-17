import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
});

export async function uploadDocument(projectId, file) {
  const form = new FormData();
  form.append("file", file);
  const res = await API.post(`/api/upload/${encodeURIComponent(projectId)}`, form);
  return res.data;
}

export async function generateTickets(projectId, promptOverride = null) {
  const res = await API.post("/api/generate", {
    project_id: projectId,
    prompt_override: promptOverride,
  });
  return res.data;
}

export async function syncToADO(projectId, workItems) {
  const res = await API.post("/api/sync", {
    project_id: projectId,
    work_items: workItems,
  });
  return res.data;
}

export async function getProjectContext(projectId) {
  const res = await API.get(`/api/projects/${encodeURIComponent(projectId)}/context`);
  return res.data;
}

export async function clearProjectContext(projectId) {
  const res = await API.delete(`/api/projects/${encodeURIComponent(projectId)}/context`);
  return res.data;
}

export async function listProjects() {
  const res = await API.get("/api/projects");
  return res.data.projects;
}

export async function listProjectFiles(projectId) {
  const res = await API.get(`/api/projects/${encodeURIComponent(projectId)}/files`);
  return res.data.files;
}

export async function deleteProjectFile(projectId, fileId) {
  const res = await API.delete(`/api/projects/${encodeURIComponent(projectId)}/files/${encodeURIComponent(fileId)}`);
  return res.data;
}

export async function getGitHubStatus() {
  const res = await API.get("/api/github/status");
  return res.data;
}

export async function getRepoPRs(state = "all") {
  const res = await API.get("/api/github/prs", { params: { state } });
  return res.data;
}

export async function getRepoContext() {
  const res = await API.get("/api/github/repo-context");
  return res.data;
}

export async function runAgent(ticket, allTickets = null) {
  const res = await API.post("/api/agent/run", { ticket, all_tickets: allTickets }, { timeout: 120000 });
  return res.data;
}
