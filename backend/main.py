import os
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import (
    GenerateRequest,
    SyncRequest,
    UploadResponse,
    ADOHierarchy,
    ADOSyncResult,
    AgentRequest,
    AgentResult,
)
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStoreService
from app.services.ai_mapper import AIMapper
from app.services.ado_client import ADOClient
from app.services.dev_agent import DevAgent

app = FastAPI(title="PO Copilot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.upload_dir, exist_ok=True)

doc_processor = DocumentProcessor()
vector_store = VectorStoreService()
ai_mapper = AIMapper()
ado_client = ADOClient()
dev_agent = DevAgent()

ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".txt", ".md", ".csv"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/upload/{project_id}", response_model=UploadResponse)
async def upload_document(project_id: str, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {ALLOWED_EXTENSIONS}",
        )

    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}{ext}"
    file_path = os.path.join(settings.upload_dir, safe_filename)

    content = await file.read()
    if len(content) > 20 * 1024 * 1024:  # 20 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds 20 MB limit")

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        chunks = doc_processor.process(file_path, ext)
        vector_store.store(project_id, chunks, file_id, file.filename or safe_filename)
    finally:
        os.remove(file_path)

    return UploadResponse(
        file_id=file_id,
        filename=file.filename or safe_filename,
        chunks_created=len(chunks),
        message="Document processed and indexed successfully.",
    )


@app.post("/api/generate", response_model=ADOHierarchy)
async def generate_tickets(req: GenerateRequest):
    context_chunks = vector_store.query(req.project_id)
    if not context_chunks:
        raise HTTPException(
            status_code=404,
            detail="No documents found for this project. Upload documents first.",
        )

    try:
        hierarchy = ai_mapper.map_to_ado(
            project_id=req.project_id,
            context=context_chunks,
            prompt_override=req.prompt_override,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")
    return hierarchy


@app.post("/api/sync", response_model=ADOSyncResult)
async def sync_to_ado(req: SyncRequest):
    if not settings.ado_pat or not settings.ado_org_url:
        raise HTTPException(
            status_code=400,
            detail="Azure DevOps credentials not configured. Set ADO_ORG_URL and ADO_PAT in .env",
        )

    result = ado_client.sync_work_items(req.project_id, req.work_items)
    return result


@app.get("/api/projects/{project_id}/context")
async def get_project_context(project_id: str):
    chunks = vector_store.query(project_id, n_results=5)
    return {"project_id": project_id, "chunk_count": len(chunks), "preview": chunks[:5]}


@app.get("/api/projects")
async def list_projects():
    return {"projects": vector_store.list_projects()}


@app.get("/api/projects/{project_id}/files")
async def list_project_files(project_id: str):
    return {"files": vector_store.list_files(project_id)}


@app.delete("/api/projects/{project_id}/files/{file_id}")
async def delete_project_file(project_id: str, file_id: str):
    deleted = vector_store.delete_file(project_id, file_id)
    return {"deleted_chunks": deleted}


# ── GitHub / Agent endpoints ──────────────────────────

@app.get("/api/github/status")
async def github_status():
    """Check if GitHub is configured and return repo info."""
    configured = bool(settings.github_token and settings.github_owner and settings.github_repo)
    return {
        "configured": configured,
        "owner": settings.github_owner if configured else None,
        "repo": settings.github_repo if configured else None,
    }


@app.post("/api/agent/run", response_model=AgentResult)
async def run_agent(req: AgentRequest):
    """Run the AI dev agent on a single ticket."""
    if not settings.github_token:
        raise HTTPException(
            status_code=400,
            detail="GitHub token not configured. Set GITHUB_TOKEN in .env",
        )
    try:
        result = dev_agent.execute(req.ticket)
        return AgentResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed: {str(e)}")


@app.delete("/api/projects/{project_id}/context")
async def clear_project_context(project_id: str):
    vector_store.clear(project_id)
    return {"message": f"Context cleared for project {project_id}"}
