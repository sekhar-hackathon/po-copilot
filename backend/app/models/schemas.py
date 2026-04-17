from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class WorkItemType(str, Enum):
    EPIC = "Epic"
    FEATURE = "Feature"
    USER_STORY = "User Story"
    TASK = "Task"


class WorkItem(BaseModel):
    type: WorkItemType
    title: str
    description: str
    acceptance_criteria: Optional[str] = None
    story_points: Optional[int] = None
    parent_title: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class ADOHierarchy(BaseModel):
    project_id: str
    epics: list[WorkItem] = Field(default_factory=list)
    features: list[WorkItem] = Field(default_factory=list)
    user_stories: list[WorkItem] = Field(default_factory=list)
    tasks: list[WorkItem] = Field(default_factory=list)


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    chunks_created: int
    message: str


class GenerateRequest(BaseModel):
    project_id: str
    prompt_override: Optional[str] = None


class SyncRequest(BaseModel):
    project_id: str
    work_items: list[WorkItem]


class ADOSyncResult(BaseModel):
    created: int
    failed: int


class AgentRequest(BaseModel):
    ticket: dict
    all_tickets: Optional[list[dict]] = None


class AgentResult(BaseModel):
    status: str
    branch: Optional[str] = None
    pr_number: Optional[int] = None
    pr_url: Optional[str] = None
    files_created: Optional[int] = None
    summary: Optional[str] = None
    message: Optional[str] = None
    errors: list[str] = Field(default_factory=list)
    created_ids: list[int] = Field(default_factory=list)
