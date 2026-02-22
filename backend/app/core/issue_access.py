from sqlalchemy.orm import Session
from app.models.issues import Issue


def get_visible_issues(db: Session, user):
    """
    Returns issues visible to user based on permissions
    """

    perms = user.permissions

    # Admin / Manager
    if "view_all" in perms:
        return db.query(Issue)

    # Engineer
    if "view_assigned" in perms:
        return db.query(Issue).filter(
            Issue.assigned_to_id == user.id
        )

    # Reporter
    if "view_own" in perms:
        return db.query(Issue).filter(
            Issue.created_by_id == user.id
        )

    # No access
    return db.query(Issue).filter(False)