import json
import httpx
import truststore
from openai import OpenAI
from app.config import settings
from app.models.schemas import ADOHierarchy, WorkItem, WorkItemType

SYSTEM_PROMPT = """You are PO Copilot, an expert Product Owner assistant. Your job is to analyze 
meeting notes, requirement documents, and other project context to structure them into Azure DevOps 
work items following the hierarchy: Epic > Feature > User Story > Task.

Rules:
1. Create a logical hierarchy - Epics contain high-level themes, Features break them down, 
   User Stories are from a user perspective, Tasks are implementation steps.
2. User Stories MUST follow the format: "As a [role], I want [goal], so that [benefit]"
3. Assign realistic story points (1, 2, 3, 5, 8, 13) using Fibonacci scale.
4. Set parent_title to link child items to their parent (Feature->Epic, Story->Feature, Task->Story).
5. Include acceptance criteria for User Stories.
6. Extract any mentioned tags/labels.

Return ONLY valid JSON matching this exact schema:
{
  "project_id": "<project_id>",
  "epics": [{"type": "Epic", "title": "...", "description": "...", "tags": []}],
  "features": [{"type": "Feature", "title": "...", "description": "...", "parent_title": "<epic_title>", "tags": []}],
  "user_stories": [{"type": "User Story", "title": "...", "description": "As a...", "acceptance_criteria": "...", "story_points": 5, "parent_title": "<feature_title>", "tags": []}],
  "tasks": [{"type": "Task", "title": "...", "description": "...", "story_points": 2, "parent_title": "<story_title>", "tags": []}]
}
"""


class AIMapper:
    """Uses OpenAI to convert unstructured text into structured ADO work items."""

    def __init__(self):
        ssl_ctx = truststore.SSLContext()
        http_client = httpx.Client(verify=ssl_ctx)
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            http_client=http_client,
        )
        self.model = settings.openai_model

    def map_to_ado(
        self,
        project_id: str,
        context: list[str],
        prompt_override: str | None = None,
    ) -> ADOHierarchy:
        combined_context = "\n\n---\n\n".join(context)

        user_prompt = prompt_override or (
            f"Analyze the following project documents and create a complete ADO work item hierarchy.\n\n"
            f"Project ID: {project_id}\n\n"
            f"=== DOCUMENT CONTEXT ===\n{combined_context}\n=== END CONTEXT ==="
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)

        def _parse_items(items: list[dict], default_type: WorkItemType) -> list[WorkItem]:
            result = []
            for item in items:
                item.pop("type", None)  # Remove type from LLM output to avoid conflict
                result.append(WorkItem(type=default_type, **item))
            return result

        return ADOHierarchy(
            project_id=project_id,
            epics=_parse_items(data.get("epics", []), WorkItemType.EPIC),
            features=_parse_items(data.get("features", []), WorkItemType.FEATURE),
            user_stories=_parse_items(data.get("user_stories", []), WorkItemType.USER_STORY),
            tasks=_parse_items(data.get("tasks", []), WorkItemType.TASK),
        )
