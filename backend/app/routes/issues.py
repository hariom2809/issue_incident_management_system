from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.issues import Issue
from app.models.users import User
from app.core.audit import log_action
from app.core.security import get_current_user, require_permission
from app.core.issue_access import get_visible_issues

ALLOWED_STATUS = ["open", "in_progress", "resolved", "closed"]

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/")
def create_issue(
    title: str,
    description: str,
    priority: str = "medium",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("create_incident"))
):
    issue = Issue(
        title=title,
        description=description,
        priority=priority,
        status="open",
        created_by_id=current_user.id
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)

    log_action(issue.id, current_user.id, "issue_created")

    return issue

@router.get("/")
def list_issues(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("view_incident"))
):
    query = get_visible_issues(db, current_user)
    return query.all()

@router.patch("/{issue_id}")
def update_issue(
    issue_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("update_incident"))
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if not can_update_issue(current_user, issue):
        raise HTTPException(status_code=403, detail="Not authorized")

    if status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")

    old_status = issue.status
    issue.status = status

    db.commit()

    log_action(
        issue.id,
        current_user.id,
        "status_changed",
        old_status,
        status
    )

    return {"message": "Issue updated"}

@router.patch("/{issue_id}/assign")
def assign_issue(
    issue_id: int,
    assigned_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("assign_incident"))
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    assigned_user = db.query(User).filter(User.id == assigned_user_id).first()
    if not assigned_user:
        raise HTTPException(status_code=404, detail="User not found")

    if issue.assigned_to_id == assigned_user.id:
        return {"message": "Issue already assigned to this user"}
    
    old_assignee = issue.assigned_to_id
    issue.assigned_to_id = assigned_user.id

    db.commit()

    log_action(
        issue.id,
        current_user.id,
        "issue_assigned",
        str(old_assignee),
        str(assigned_user.id)
    )

    return {
        "message": f"Issue assigned to user {assigned_user.id}"
    }

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.id,
        "permissions": current_user.permissions
    }
