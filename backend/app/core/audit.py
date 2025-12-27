from models.audit_log import AuditLog
from database.database import SessionLocal

def log_action(issue_id, user_id, action, old_value=None, new_value=None):
    db = SessionLocal()
    log = AuditLog(
        issue_id=issue_id,
        user_id=user_id,
        action=action,
        old_value=str(old_value) if old_value else None,
        new_value=str(new_value) if new_value else None
    )
    db.add(log)
    db.commit()
    db.close()
