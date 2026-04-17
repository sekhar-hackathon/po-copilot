"""
AI Dev Agent — takes a work item ticket, generates code using LLM,
creates a feature branch on GitHub, commits files, and opens a PR.
"""

import json
import re
import base64
import httpx
import truststore
from openai import OpenAI
from app.config import settings

CODE_GEN_PROMPT = """You are a senior software engineer AI agent. You have been assigned a ticket
from a product backlog. Your job is to implement the ticket by generating production-ready code.

Given the ticket details, generate the code files needed to implement the requirement.

Rules:
1. Generate clean, well-structured, production-ready code.
2. Include proper imports and type hints.
3. Add brief inline comments only where logic is non-obvious.
4. Follow best practices for the language/framework.
5. If the ticket is a User Story, implement it end-to-end.
6. If the ticket is a Task, implement the specific task described.
7. Generate test files where appropriate.

Return ONLY valid JSON with this schema:
{
  "files": [
    {
      "path": "src/path/to/file.py",
      "content": "full file content here",
      "description": "brief description of what this file does"
    }
  ],
  "summary": "Brief summary of what was implemented",
  "pr_description": "Markdown description for the pull request"
}
"""


class DevAgent:
    """AI-powered developer agent that creates code and PRs from tickets."""

    def __init__(self):
        ssl_ctx = truststore.SSLContext()
        http_client = httpx.Client(verify=ssl_ctx)
        self.llm = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            http_client=http_client,
        )
        self.model = settings.openai_model
        self.github_token = settings.github_token
        self.owner = settings.github_owner
        self.repo = settings.github_repo
        self.api_base = "https://api.github.com"

    def _gh_headers(self):
        return {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _gh_request(self, method, path, **kwargs):
        ssl_ctx = truststore.SSLContext()
        with httpx.Client(verify=ssl_ctx) as client:
            resp = client.request(
                method,
                f"{self.api_base}{path}",
                headers=self._gh_headers(),
                **kwargs,
            )
            resp.raise_for_status()
            return resp.json() if resp.content else {}

    def _sanitize_branch_name(self, title: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
        return f"agent/{slug[:50]}"

    # ── GitHub operations ──────────────────────────────────

    def _get_default_branch(self) -> str:
        repo = self._gh_request("GET", f"/repos/{self.owner}/{self.repo}")
        return repo["default_branch"]

    def _get_branch_sha(self, branch: str) -> str:
        ref = self._gh_request("GET", f"/repos/{self.owner}/{self.repo}/git/ref/heads/{branch}")
        return ref["object"]["sha"]

    def _create_branch(self, branch_name: str, from_sha: str):
        self._gh_request(
            "POST",
            f"/repos/{self.owner}/{self.repo}/git/refs",
            json={"ref": f"refs/heads/{branch_name}", "sha": from_sha},
        )

    def _commit_files(self, branch: str, files: list[dict], message: str):
        """Create a commit with multiple files using the Git trees API."""
        # Get current commit & tree
        sha = self._get_branch_sha(branch)
        commit = self._gh_request("GET", f"/repos/{self.owner}/{self.repo}/git/commits/{sha}")
        base_tree = commit["tree"]["sha"]

        # Build tree entries
        tree_items = []
        for f in files:
            blob = self._gh_request(
                "POST",
                f"/repos/{self.owner}/{self.repo}/git/blobs",
                json={"content": f["content"], "encoding": "utf-8"},
            )
            tree_items.append({
                "path": f["path"],
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"],
            })

        # Create tree
        new_tree = self._gh_request(
            "POST",
            f"/repos/{self.owner}/{self.repo}/git/trees",
            json={"base_tree": base_tree, "tree": tree_items},
        )

        # Create commit
        new_commit = self._gh_request(
            "POST",
            f"/repos/{self.owner}/{self.repo}/git/commits",
            json={
                "message": message,
                "tree": new_tree["sha"],
                "parents": [sha],
            },
        )

        # Update branch ref
        self._gh_request(
            "PATCH",
            f"/repos/{self.owner}/{self.repo}/git/refs/heads/{branch}",
            json={"sha": new_commit["sha"]},
        )

    def _create_pr(self, branch: str, title: str, body: str, base: str) -> dict:
        return self._gh_request(
            "POST",
            f"/repos/{self.owner}/{self.repo}/pulls",
            json={"title": title, "body": body, "head": branch, "base": base},
        )

    # ── Main agent flow ────────────────────────────────────

    def generate_code(self, ticket: dict) -> dict:
        """Use LLM to generate code for the given ticket."""
        user_prompt = (
            f"Implement the following ticket:\n\n"
            f"**Type**: {ticket['type']}\n"
            f"**Title**: {ticket['title']}\n"
            f"**Description**: {ticket['description']}\n"
        )
        if ticket.get("acceptance_criteria"):
            user_prompt += f"**Acceptance Criteria**: {ticket['acceptance_criteria']}\n"
        if ticket.get("parent_title"):
            user_prompt += f"**Parent**: {ticket['parent_title']}\n"
        if ticket.get("tags"):
            user_prompt += f"**Tags**: {', '.join(ticket['tags'])}\n"

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": CODE_GEN_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content or "{}"
        return json.loads(raw)

    def execute(self, ticket: dict) -> dict:
        """Full agent pipeline: generate code → branch → commit → PR."""
        # 1. Generate code
        gen_result = self.generate_code(ticket)
        files = gen_result.get("files", [])
        summary = gen_result.get("summary", "AI-generated implementation")
        pr_body = gen_result.get("pr_description", summary)

        if not files:
            return {
                "status": "error",
                "message": "Agent could not generate any code for this ticket.",
            }

        # 2. Create branch
        default_branch = self._get_default_branch()
        base_sha = self._get_branch_sha(default_branch)
        branch_name = self._sanitize_branch_name(ticket["title"])

        # Check if branch already exists, append suffix if so
        try:
            self._get_branch_sha(branch_name)
            import time
            branch_name = f"{branch_name}-{int(time.time()) % 10000}"
        except httpx.HTTPStatusError:
            pass  # Branch doesn't exist, good

        self._create_branch(branch_name, base_sha)

        # 3. Commit files
        commit_msg = f"feat: {ticket['title']}\n\nImplemented by PO Copilot AI Agent\n\n{summary}"
        self._commit_files(branch_name, files, commit_msg)

        # 4. Open PR
        pr_title = f"🤖 [{ticket['type']}] {ticket['title']}"

        # Build ticket details section (like AD#1234 references)
        ticket_details = (
            f"| Field | Value |\n"
            f"|-------|-------|\n"
            f"| **Type** | {ticket['type']} |\n"
            f"| **Title** | {ticket['title']} |\n"
        )
        if ticket.get("parent_title"):
            ticket_details += f"| **Parent** | {ticket['parent_title']} |\n"
        if ticket.get("acceptance_criteria"):
            ticket_details += f"| **Acceptance Criteria** | {ticket['acceptance_criteria']} |\n"
        if ticket.get("story_points"):
            ticket_details += f"| **Story Points** | {ticket['story_points']} |\n"
        if ticket.get("tags"):
            ticket_details += f"| **Tags** | {', '.join(ticket['tags'])} |\n"

        pr_body_full = (
            f"## 🤖 AI Agent Implementation\n\n"
            f"### 📋 Ticket Details\n\n"
            f"{ticket_details}\n"
            f"> **Description**: {ticket.get('description', 'N/A')}\n\n"
            f"---\n\n"
            f"### 🔗 Hierarchy\n\n"
            f"- **Parent**: {ticket.get('parent_title', 'None (top-level)')}\n"
            f"- **Type**: {ticket['type']}\n"
            f"- **Ticket**: {ticket['title']}\n\n"
            f"---\n\n"
            f"### 📝 Implementation Summary\n\n"
            f"{pr_body}\n\n"
            f"---\n\n"
            f"### 📁 Files Changed\n\n"
            + "\n".join(f"- `{f['path']}` — {f.get('description', '')}" for f in files)
            + "\n\n---\n\n"
            f"*🤖 This PR was automatically created by **PO Copilot AI Dev Agent** — Team Diamond × SKF*"
        )

        pr = self._create_pr(branch_name, pr_title, pr_body_full, default_branch)

        return {
            "status": "success",
            "branch": branch_name,
            "pr_number": pr["number"],
            "pr_url": pr["html_url"],
            "files_created": len(files),
            "summary": summary,
        }
