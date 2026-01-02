from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.issues import Issue
from app.models.users import User
from app.core.audit import log_action
from app.core.permissions import can_update_issue

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/")
def create_issue(title: str, description: str, priority: str = "medium", db: Session = Depends(get_db)):
    issue = Issue(
        title=title,
        description=description,
        priority=priority,
        status="open",
        created_by_id=1   # Temporary user (will be replaced by JWT later)
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)

    log_action(issue.id, issue.created_by_id, "issue_created")

    return issue

@router.get("/")
def list_issues(db: Session = Depends(get_db)):
    return db.query(Issue).all()

@router.patch("/{issue_id}")
def update_issue(issue_id: int, status: str, db: Session = Depends(get_db)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    old_status = issue.status
    issue.status = status

    db.commit()

    log_action(issue.id, issue.assigned_to_id, "status_changed", old_status, status)

    current_user = db.query(User).filter(User.id == 1).first()
    if not can_update_issue(current_user, issue):
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"message": "Issue updated"}
