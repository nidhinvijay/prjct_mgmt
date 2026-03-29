from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus, TaskUpdateAssignee

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify project exists
    result = await db.execute(select(Project).filter(Project.id == task_in.project_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")
        
    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        project_id=task_in.project_id,
        assigned_to=task_in.assigned_to,
        due_date=task_in.due_date
        # status defaults to "To Do"
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.patch("/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: int, 
    assign_in: TaskUpdateAssignee, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify User exists before assigning
    user_res = await db.execute(select(User).filter(User.id == assign_in.assigned_to))
    if not user_res.scalars().first():
        raise HTTPException(status_code=404, detail="Assignee User not found")

    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.assigned_to = assign_in.assigned_to
    await db.commit()
    await db.refresh(task)
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int, 
    status_in: TaskUpdateStatus, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = status_in.status
    await db.commit()
    await db.refresh(task)
    return task

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1, le=100), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Task)
    
    # Advanced Requirement: Filtering
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    if status is not None:
        query = query.filter(Task.status == status)
    if assigned_to is not None:
        query = query.filter(Task.assigned_to == assigned_to)
        
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    
    return result.scalars().all()
