from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.audit_log import AuditLog
from app.core.security import get_current_user
from app.models.users import User


router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/{issue_id}")
def get_issue_timeline(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.issue_id == issue_id)
        .order_by(AuditLog.created_at.asc())
        .all()
    )
    return logs
