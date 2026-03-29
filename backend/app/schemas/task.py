from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdateStatus(BaseModel):
    status: str

class TaskUpdateAssignee(BaseModel):
    assigned_to: int

class TaskResponse(TaskBase):
    id: int
    status: str

    class Config:
        from_attributes = True
