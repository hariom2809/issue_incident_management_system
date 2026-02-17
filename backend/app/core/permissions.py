from fastapi import HTTPException

def can_update_issue(user, issue):
    user_roles = [ur.role.name for ur in user.user_roles]

    if "admin" in user_roles:
        return True

    if "engineer" in user_roles and issue.assigned_to_id == user.id:
        return True

    if "reporter" in user_roles and issue.created_by_id == user.id:
        return True

    return False

def get_user_permissions(user):
    """
    Extract all permissions from user roles.
    User → UserRole → Role → RolePermission → Permission
    """

    permissions = set()

    for user_role in user.user_roles:
        role = user_role.role

        for rp in role.role_permissions:
            permissions.add(rp.permission.name)

    return list(permissions)

def has_permission(user, permission: str) -> bool:
    return permission in getattr(user, "permissions", [])