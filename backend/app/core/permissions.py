from fastapi import HTTPException

def can_update_issue(user, issue):
    user_roles = [ur.role.name for ur in user.roles]

    if "admin" in user_roles:
        return True

    if "engineer" in user_roles and issue.assigned_to_id == user.id:
        return True

    if "reporter" in user_roles and issue.created_by_id == user.id:
        return True

    return False
