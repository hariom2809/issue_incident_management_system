from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.issues_comments import IssueComment
from app.models.issues import Issue
from app.models.users import User
from app.core.security import require_permission
from app.core.audit import log_action

router = APIRouter(prefix="/issues", tags=["Comments"])


@router.post("/{issue_id}/comments")
def add_comment(
    issue_id: int,
    comment: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("comment_incident"))
):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(404, "Issue not found")

    new_comment = IssueComment(
        issue_id=issue_id,
        user_id=current_user.id,
        comment=comment
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    log_action(issue_id, current_user.id, "comment_added")

    return new_comment


@router.get("/{issue_id}/comments")
def list_comments(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("comment_incident"))
):
    return (
        db.query(IssueComment)
        .filter(IssueComment.issue_id == issue_id)
        .order_by(IssueComment.created_at.asc())
        .all()
    )