# PO Copilot

AI-powered Product Owner assistant that transforms unstructured meeting notes (MOM) and requirement documents into actionable Azure DevOps work items.

## Architecture

```
Upload Documents → Process & Chunk → Store in Vector DB → AI Analysis → ADO Ticket Hierarchy → Human Review → Sync to Azure DevOps
```

### Tech Stack
- **Frontend:** React.js + Tailwind CSS
- **Backend:** Python FastAPI
- **Vector DB:** ChromaDB
- **AI/LLM:** OpenAI GPT-4o via LangChain
- **Integration:** Azure DevOps REST API

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Edit `backend/.env` with your credentials:
- `OPENAI_API_KEY` — your OpenAI API key
- `ADO_ORG_URL` — e.g. `https://dev.azure.com/YOUR_ORG`
- `ADO_PAT` — Azure DevOps Personal Access Token
- `ADO_PROJECT` — your ADO project name

Run the backend:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

## Usage

1. **Enter a Project ID** in the header (any unique identifier for your project).
2. **Upload documents** — meeting notes, PDFs, spreadsheets, or text files.
3. **Click "Generate Tickets"** — the AI analyzes your documents and produces a full Epic → Feature → User Story → Task hierarchy.
4. **Review & Edit** — modify titles, descriptions, story points, or remove items.
5. **Sync to ADO** — push approved tickets to your Azure DevOps board.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/{project_id}` | Upload and index a document |
| POST | `/api/generate` | Generate ADO work item hierarchy from indexed docs |
| POST | `/api/sync` | Push work items to Azure DevOps |
| GET | `/api/projects/{project_id}/context` | Preview indexed chunks |
| DELETE | `/api/projects/{project_id}/context` | Clear project context |
