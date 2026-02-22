from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.audit_log import AuditLog
from app.models.issues import Issue
from app.core.security import get_current_user
from app.models.users import User
from app.core.issue_access import can_view_issue

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/{issue_id}")
def get_issue_timeline(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(404, "Issue not found")

    if not can_view_issue(current_user, issue):
        raise HTTPException(403, "Not authorized")

    logs = (
        db.query(AuditLog)
        .filter(AuditLog.issue_id == issue_id)
        .order_by(AuditLog.created_at.asc())
        .all()
    )

    return logs