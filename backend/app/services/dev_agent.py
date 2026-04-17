"""
AI Dev Agent v0.2 — Enhanced with repo context, PR history,
parent/child ticket awareness, and code navigation.
"""

import json
import re
import time
import httpx
import truststore
from openai import OpenAI
from app.config import settings

CODE_GEN_PROMPT = """You are a senior software engineer AI agent working on the repository "{owner}/{repo}".
You have been assigned a ticket from a product backlog. Your job is to implement the ticket by generating production-ready code.

## Repository Context
{repo_context}

## Related Tickets Context
{tickets_context}

## Previously Created PRs
{pr_context}

Rules:
1. Generate clean, well-structured, production-ready code.
2. Include proper imports and type hints.
3. Add brief inline comments only where logic is non-obvious.
4. Follow best practices for the language/framework.
5. If the ticket is a User Story, implement it end-to-end.
6. If the ticket is a Task, implement the specific task described.
7. Generate test files where appropriate.
8. If there is existing code in the repo that relates to this ticket, reference the existing file paths and build upon them rather than creating duplicate files.
9. If a parent or sibling ticket has already been implemented (has a PR), make sure your implementation is compatible with and builds upon that work.
10. Include updates to existing test files if applicable.

Return ONLY valid JSON with this schema:
{{
  "files": [
    {{
      "path": "src/path/to/file.py",
      "content": "full file content here",
      "description": "brief description of what this file does"
    }}
  ],
  "summary": "Brief summary of what was implemented",
  "pr_description": "Markdown description for the pull request",
  "related_files_analyzed": ["list of existing repo files you considered"]
}}
"""


class DevAgent:
    """AI-powered developer agent with repo context and PR history awareness."""

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
        with httpx.Client(verify=ssl_ctx, timeout=30) as client:
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

    # ── Repo Context & PR History ──────────────────────────

    def list_prs(self, state: str = "all", per_page: int = 30) -> list[dict]:
        """List PRs from the repo (open, closed, or all)."""
        raw = self._gh_request(
            "GET",
            f"/repos/{self.owner}/{self.repo}/pulls",
            params={"state": state, "per_page": per_page, "sort": "updated", "direction": "desc"},
        )
        return [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "merged": pr.get("merged_at") is not None,
                "html_url": pr["html_url"],
                "branch": pr["head"]["ref"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "user": pr["user"]["login"],
                "labels": [l["name"] for l in pr.get("labels", [])],
            }
            for pr in raw
        ]

    def _get_repo_tree(self) -> list[str]:
        """Get the file tree of the repo's default branch."""
        try:
            default_branch = self._get_default_branch()
            tree = self._gh_request(
                "GET",
                f"/repos/{self.owner}/{self.repo}/git/trees/{default_branch}",
                params={"recursive": "1"},
            )
            return [item["path"] for item in tree.get("tree", []) if item["type"] == "blob"][:200]
        except Exception:
            return []

    def get_repo_context(self) -> dict:
        """Get full repo analysis for the frontend."""
        try:
            repo_info = self._gh_request("GET", f"/repos/{self.owner}/{self.repo}")
        except Exception:
            repo_info = {}

        file_tree = self._get_repo_tree()
        prs = self.list_prs(state="all", per_page=20)
        open_prs = [p for p in prs if p["state"] == "open"]
        closed_prs = [p for p in prs if p["state"] == "closed"]

        return {
            "repo": f"{self.owner}/{self.repo}",
            "description": repo_info.get("description", ""),
            "default_branch": repo_info.get("default_branch", "main"),
            "language": repo_info.get("language", ""),
            "file_tree": file_tree,
            "file_count": len(file_tree),
            "open_prs": open_prs,
            "closed_prs": closed_prs,
            "total_prs": len(prs),
        }

    def _build_repo_context_prompt(self) -> str:
        """Build a concise repo context string for the LLM prompt."""
        try:
            file_tree = self._get_repo_tree()
            prs = self.list_prs(state="all", per_page=15)

            parts = [f"Repository: {self.owner}/{self.repo}"]
            if file_tree:
                parts.append(f"\nExisting files in repo ({len(file_tree)} total):")
                for f in file_tree[:100]:
                    parts.append(f"  - {f}")
                if len(file_tree) > 100:
                    parts.append(f"  ... and {len(file_tree) - 100} more files")

            if prs:
                parts.append(f"\nRecent PRs ({len(prs)} total):")
                for pr in prs[:10]:
                    status = "MERGED" if pr["merged"] else pr["state"].upper()
                    parts.append(f"  - PR #{pr['number']} [{status}]: {pr['title']} (branch: {pr['branch']})")

            return "\n".join(parts)
        except Exception:
            return f"Repository: {self.owner}/{self.repo} (could not fetch details)"

    def _build_tickets_context(self, ticket: dict, all_tickets: list[dict] | None) -> str:
        """Build context about related parent/child/sibling tickets."""
        if not all_tickets:
            return "No other ticket context available."

        current_title = ticket["title"]
        current_parent = ticket.get("parent_title", "")
        parts = []

        # Find parent ticket
        if current_parent:
            parent = next((t for t in all_tickets if t.get("title") == current_parent), None)
            if parent:
                status = "DONE (PR created)" if parent.get("_agent_status") == "done" else parent.get("_agent_status", "pending")
                parts.append(f"PARENT TICKET [{status.upper()}]: [{parent.get('type')}] {parent['title']}")
                if parent.get("description"):
                    parts.append(f"  Description: {parent['description']}")

        # Find sibling tickets (same parent)
        siblings = [t for t in all_tickets if t.get("parent_title") == current_parent and t.get("title") != current_title]
        if siblings:
            parts.append(f"\nSIBLING TICKETS (same parent '{current_parent}'):")
            for sib in siblings:
                status = "DONE (PR created)" if sib.get("_agent_status") == "done" else sib.get("_agent_status", "pending")
                parts.append(f"  - [{status.upper()}] [{sib.get('type')}] {sib['title']}")

        # Find child tickets
        children = [t for t in all_tickets if t.get("parent_title") == current_title]
        if children:
            parts.append(f"\nCHILD TICKETS:")
            for child in children:
                status = "DONE (PR created)" if child.get("_agent_status") == "done" else child.get("_agent_status", "pending")
                parts.append(f"  - [{status.upper()}] [{child.get('type')}] {child['title']}")

        if not parts:
            return "This ticket has no related parent/child/sibling tickets."

        return "\n".join(parts)

    def _build_pr_context(self) -> str:
        """Build a context string about existing PRs."""
        try:
            prs = self.list_prs(state="all", per_page=10)
            if not prs:
                return "No PRs exist yet in this repository."
            parts = ["Previously created PRs:"]
            for pr in prs:
                status = "MERGED" if pr["merged"] else pr["state"].upper()
                parts.append(f"  - PR #{pr['number']} [{status}]: {pr['title']}")
            return "\n".join(parts)
        except Exception:
            return "Could not fetch PR history."

    # ── Main agent flow ────────────────────────────────────

    def generate_code(self, ticket: dict, all_tickets: list[dict] | None = None) -> dict:
        """Use LLM to generate code with full repo and ticket context."""
        repo_context = self._build_repo_context_prompt()
        tickets_context = self._build_tickets_context(ticket, all_tickets)
        pr_context = self._build_pr_context()

        system_prompt = CODE_GEN_PROMPT.format(
            owner=self.owner,
            repo=self.repo,
            repo_context=repo_context,
            tickets_context=tickets_context,
            pr_context=pr_context,
        )

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
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content or "{}"
        return json.loads(raw)

    def execute(self, ticket: dict, all_tickets: list[dict] | None = None) -> dict:
        """Full agent pipeline: analyze repo -> generate code -> branch -> commit -> PR."""
        # 1. Generate code with full context
        gen_result = self.generate_code(ticket, all_tickets)
        files = gen_result.get("files", [])
        summary = gen_result.get("summary", "AI-generated implementation")
        pr_body = gen_result.get("pr_description", summary)
        analyzed_files = gen_result.get("related_files_analyzed", [])

        if not files:
            return {
                "status": "error",
                "message": "Agent could not generate any code for this ticket.",
            }

        # 2. Create branch
        default_branch = self._get_default_branch()
        base_sha = self._get_branch_sha(default_branch)
        branch_name = self._sanitize_branch_name(ticket["title"])

        try:
            self._get_branch_sha(branch_name)
            branch_name = f"{branch_name}-{int(time.time()) % 10000}"
        except httpx.HTTPStatusError:
            pass

        self._create_branch(branch_name, base_sha)

        # 3. Commit files
        commit_msg = f"feat: {ticket['title']}\n\nImplemented by PO Copilot AI Agent v0.2\n\n{summary}"
        self._commit_files(branch_name, files, commit_msg)

        # 4. Build rich PR body
        pr_title = f"\U0001f916 [{ticket['type']}] {ticket['title']}"

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

        # Build related tickets section
        related_section = ""
        if all_tickets:
            parent = ticket.get("parent_title", "")
            siblings = [t for t in all_tickets if t.get("parent_title") == parent and t.get("title") != ticket["title"]]
            children = [t for t in all_tickets if t.get("parent_title") == ticket["title"]]

            if parent or siblings or children:
                related_section = "### \U0001f517 Related Tickets\n\n"
                if parent:
                    related_section += f"**Parent**: {parent}\n\n"
                if siblings:
                    related_section += "**Siblings** (same parent):\n"
                    for s in siblings[:5]:
                        status_emoji = "\u2705" if s.get("_agent_status") == "done" else "\u23f3"
                        related_section += f"- {status_emoji} [{s.get('type')}] {s['title']}\n"
                    related_section += "\n"
                if children:
                    related_section += "**Children**:\n"
                    for c in children[:5]:
                        status_emoji = "\u2705" if c.get("_agent_status") == "done" else "\u23f3"
                        related_section += f"- {status_emoji} [{c.get('type')}] {c['title']}\n"
                    related_section += "\n"

        analyzed_section = ""
        if analyzed_files:
            analyzed_section = (
                "### \U0001f50d Existing Files Analyzed\n\n"
                + "\n".join(f"- `{f}`" for f in analyzed_files[:10])
                + "\n\n"
            )

        pr_body_full = (
            f"## \U0001f916 AI Agent Implementation\n\n"
            f"### \U0001f4cb Ticket Details\n\n"
            f"{ticket_details}\n"
            f"> **Description**: {ticket.get('description', 'N/A')}\n\n"
            f"---\n\n"
            f"{related_section}"
            f"---\n\n"
            f"### \U0001f4dd Implementation Summary\n\n"
            f"{pr_body}\n\n"
            f"---\n\n"
            f"{analyzed_section}"
            f"### \U0001f4c1 Files Changed\n\n"
            + "\n".join(f"- `{f['path']}` \u2014 {f.get('description', '')}" for f in files)
            + "\n\n---\n\n"
            f"*\U0001f916 This PR was automatically created by **PO Copilot AI Dev Agent v0.2** \u2014 Team Diamond \u00d7 SKF*"
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
