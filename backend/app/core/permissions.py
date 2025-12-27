from fastapi import HTTPException

def can_update_issue(user, issue):
    if user.role == "admin":
        return True
    if user.role == "engineer" and issue.assigned_to == user.id:
        return True
    if user.role == "reporter" and issue.created_by == user.id:
        return True
    return False
