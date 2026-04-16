import base64
import requests
from app.config import settings
from app.models.schemas import WorkItem, WorkItemType, ADOSyncResult


class ADOClient:
    """Client for Azure DevOps REST API to create work items."""

    def __init__(self):
        self.org_url = settings.ado_org_url.rstrip("/")
        self.project = settings.ado_project
        self.pat = settings.ado_pat

    def _headers(self) -> dict:
        token = base64.b64encode(f":{self.pat}".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json-patch+json",
        }

    def _api_url(self, work_item_type: str) -> str:
        return (
            f"{self.org_url}/{self.project}/_apis/wit/workitems/"
            f"${work_item_type}?api-version=7.1"
        )

    def _build_patch(self, item: WorkItem) -> list[dict]:
        patch = [
            {"op": "add", "path": "/fields/System.Title", "value": item.title},
            {"op": "add", "path": "/fields/System.Description", "value": item.description},
        ]
        if item.story_points and item.type in (WorkItemType.USER_STORY, WorkItemType.TASK):
            field = (
                "Microsoft.VSTS.Scheduling.StoryPoints"
                if item.type == WorkItemType.USER_STORY
                else "Microsoft.VSTS.Scheduling.RemainingWork"
            )
            patch.append({"op": "add", "path": f"/fields/{field}", "value": item.story_points})

        if item.acceptance_criteria:
            patch.append({
                "op": "add",
                "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
                "value": item.acceptance_criteria,
            })

        if item.tags:
            patch.append({
                "op": "add",
                "path": "/fields/System.Tags",
                "value": "; ".join(item.tags),
            })

        return patch

    def _create_work_item(self, item: WorkItem) -> int:
        url = self._api_url(item.type.value)
        patch = self._build_patch(item)
        resp = requests.post(url, json=patch, headers=self._headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()["id"]

    def _link_parent(self, child_id: int, parent_id: int):
        url = (
            f"{self.org_url}/{self.project}/_apis/wit/workitems/"
            f"{child_id}?api-version=7.1"
        )
        patch = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{self.org_url}/_apis/wit/workItems/{parent_id}",
            },
        }]
        resp = requests.patch(url, json=patch, headers=self._headers(), timeout=30)
        resp.raise_for_status()

    def sync_work_items(self, project_id: str, work_items: list[WorkItem]) -> ADOSyncResult:
        result = ADOSyncResult(created=0, failed=0)
        title_to_id: dict[str, int] = {}

        # Process in hierarchy order: Epics -> Features -> Stories -> Tasks
        order = [WorkItemType.EPIC, WorkItemType.FEATURE, WorkItemType.USER_STORY, WorkItemType.TASK]
        sorted_items = sorted(work_items, key=lambda w: order.index(w.type))

        for item in sorted_items:
            try:
                item_id = self._create_work_item(item)
                title_to_id[item.title] = item_id
                result.created_ids.append(item_id)
                result.created += 1

                # Link to parent if specified and parent was already created
                if item.parent_title and item.parent_title in title_to_id:
                    self._link_parent(item_id, title_to_id[item.parent_title])

            except Exception as e:
                result.failed += 1
                result.errors.append(f"Failed to create '{item.title}': {str(e)}")

        return result
