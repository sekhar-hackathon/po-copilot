"""
Push sample scaffold code to the po-copilot GitHub repo.
Run: python push_sample_code.py

Requires GITHUB_TOKEN and GITHUB_OWNER in .env
"""

import os
import json
import base64
import httpx
import truststore
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN", "")
OWNER = os.getenv("GITHUB_OWNER", "")
REPO = os.getenv("GITHUB_REPO", "po-copilot")
API = "https://api.github.com"

SAMPLE_FILES = [
    {
        "path": "README.md",
        "content": """# PO Copilot - AI-Powered Product Owner Assistant

An intelligent assistant that transforms meeting notes and requirement documents into structured Azure DevOps work items, with AI dev agents that can implement tickets automatically.

## Features

- **Document Upload & RAG**: Upload meeting notes, requirements, spreadsheets — processed and indexed via vector embeddings
- **AI Ticket Generation**: GPT-4o analyzes documents and creates Epic > Feature > User Story > Task hierarchy
- **Kanban Board**: Visual board with To Do / In Progress / Done columns
- **AI Dev Agent**: Assign an AI agent to a ticket — it generates code, creates a branch, and opens a PR
- **Azure DevOps Sync**: Push work items directly to ADO boards (optional)

## Tech Stack

- **Backend**: Python, FastAPI, ChromaDB, OpenAI SDK
- **Frontend**: React 18, Vite, Tailwind CSS
- **AI**: GPT-4o via OpenRouter / Azure AI Foundry
- **Version Control**: GitHub API for branch/commit/PR automation

## Quick Start

```bash
# Backend
cd backend
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install && npm run dev
```

## Architecture

```
Documents → RAG Pipeline → Vector Store (ChromaDB)
                                ↓
                     AI Mapper (GPT-4o) → ADO Hierarchy
                                ↓
                     Kanban Board (React) → AI Dev Agent → GitHub PR
```

## License

MIT — Built for SKF Hackathon 2026
""",
    },
    {
        "path": "src/__init__.py",
        "content": '"""PO Copilot - AI-Powered Product Owner Assistant"""\n\n__version__ = "1.0.0"\n',
    },
    {
        "path": "src/config.py",
        "content": """\"\"\"Application configuration.\"\"\"
import os

# Application settings
APP_NAME = "PO Copilot"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
""",
    },
    {
        "path": "src/models.py",
        "content": """\"\"\"Data models for PO Copilot.\"\"\"
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class WorkItemType(str, Enum):
    EPIC = "Epic"
    FEATURE = "Feature"
    USER_STORY = "User Story"
    TASK = "Task"


class TicketStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@dataclass
class WorkItem:
    type: WorkItemType
    title: str
    description: str
    acceptance_criteria: Optional[str] = None
    story_points: Optional[int] = None
    parent_title: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    status: TicketStatus = TicketStatus.TODO


@dataclass
class ProjectBacklog:
    project_id: str
    epics: list[WorkItem] = field(default_factory=list)
    features: list[WorkItem] = field(default_factory=list)
    user_stories: list[WorkItem] = field(default_factory=list)
    tasks: list[WorkItem] = field(default_factory=list)
""",
    },
    {
        "path": "src/utils.py",
        "content": """\"\"\"Utility functions for PO Copilot.\"\"\"


def sanitize_branch_name(title: str) -> str:
    \"\"\"Convert a ticket title to a valid git branch name.\"\"\"
    import re
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return f"agent/{slug[:50]}"


def estimate_story_points(description: str) -> int:
    \"\"\"Simple heuristic for story point estimation.\"\"\"
    word_count = len(description.split())
    if word_count < 20:
        return 1
    elif word_count < 50:
        return 3
    elif word_count < 100:
        return 5
    else:
        return 8
""",
    },
    {
        "path": "tests/__init__.py",
        "content": "",
    },
    {
        "path": "tests/test_models.py",
        "content": """\"\"\"Tests for data models.\"\"\"
from src.models import WorkItem, WorkItemType, TicketStatus


def test_work_item_creation():
    item = WorkItem(
        type=WorkItemType.USER_STORY,
        title="As a user, I want to upload documents",
        description="Upload meeting notes for AI analysis",
        story_points=5,
        tags=["upload", "documents"],
    )
    assert item.type == WorkItemType.USER_STORY
    assert item.story_points == 5
    assert item.status == TicketStatus.TODO
    assert len(item.tags) == 2


def test_work_item_defaults():
    item = WorkItem(
        type=WorkItemType.TASK,
        title="Set up CI/CD",
        description="Configure GitHub Actions pipeline",
    )
    assert item.acceptance_criteria is None
    assert item.story_points is None
    assert item.parent_title is None
    assert item.tags == []
""",
    },
    {
        "path": ".gitignore",
        "content": """__pycache__/
*.py[cod]
.env
.venv/
node_modules/
dist/
*.egg-info/
.chroma_data/
uploads/
""",
    },
]


def main():
    if not TOKEN or not OWNER:
        print("ERROR: Set GITHUB_TOKEN and GITHUB_OWNER in .env first!")
        print("  GITHUB_TOKEN = your GitHub Personal Access Token (needs 'repo' scope)")
        print("  GITHUB_OWNER = your GitHub username")
        return

    ssl_ctx = truststore.SSLContext()

    with httpx.Client(verify=ssl_ctx) as client:
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        # 1. Check if repo exists, create if not
        print(f"Checking if {OWNER}/{REPO} exists...")
        resp = client.get(f"{API}/repos/{OWNER}/{REPO}", headers=headers)

        if resp.status_code == 404:
            print(f"Creating repo '{REPO}'...")
            create_resp = client.post(
                f"{API}/user/repos",
                headers=headers,
                json={
                    "name": REPO,
                    "description": "PO Copilot - AI-Powered Product Owner Assistant | SKF Hackathon 2026",
                    "private": False,
                    "auto_init": True,
                },
            )
            create_resp.raise_for_status()
            print(f"Repo created: https://github.com/{OWNER}/{REPO}")
            import time
            time.sleep(2)  # Wait for GitHub to initialize repo
        elif resp.status_code == 200:
            print(f"Repo already exists: https://github.com/{OWNER}/{REPO}")
        else:
            print(f"Error checking repo: {resp.status_code} {resp.text}")
            return

        # 2. Get default branch SHA
        repo_info = client.get(f"{API}/repos/{OWNER}/{REPO}", headers=headers).json()
        default_branch = repo_info["default_branch"]
        ref = client.get(
            f"{API}/repos/{OWNER}/{REPO}/git/ref/heads/{default_branch}", headers=headers
        ).json()
        base_sha = ref["object"]["sha"]
        commit = client.get(
            f"{API}/repos/{OWNER}/{REPO}/git/commits/{base_sha}", headers=headers
        ).json()
        base_tree = commit["tree"]["sha"]

        # 3. Create blobs and tree
        print("Uploading sample files...")
        tree_items = []
        for f in SAMPLE_FILES:
            blob = client.post(
                f"{API}/repos/{OWNER}/{REPO}/git/blobs",
                headers=headers,
                json={"content": f["content"], "encoding": "utf-8"},
            ).json()
            tree_items.append({
                "path": f["path"],
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"],
            })
            print(f"  ✓ {f['path']}")

        # 4. Create tree
        new_tree = client.post(
            f"{API}/repos/{OWNER}/{REPO}/git/trees",
            headers=headers,
            json={"base_tree": base_tree, "tree": tree_items},
        ).json()

        # 5. Create commit
        new_commit = client.post(
            f"{API}/repos/{OWNER}/{REPO}/git/commits",
            headers=headers,
            json={
                "message": "feat: initial PO Copilot scaffold\n\nAdded project structure, models, utilities, tests, and README.\nCreated by PO Copilot setup script.",
                "tree": new_tree["sha"],
                "parents": [base_sha],
            },
        ).json()

        # 6. Update branch ref
        client.patch(
            f"{API}/repos/{OWNER}/{REPO}/git/refs/heads/{default_branch}",
            headers=headers,
            json={"sha": new_commit["sha"]},
        )

        print(f"\n✅ Sample code pushed to https://github.com/{OWNER}/{REPO}")
        print(f"   Commit: {new_commit['sha'][:8]}")
        print(f"   Files: {len(SAMPLE_FILES)}")


if __name__ == "__main__":
    main()
