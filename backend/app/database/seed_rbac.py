from app.database.database import SessionLocal
from app.models.rbac import Role, Permission, RolePermission

def seed_rbac():
    db = SessionLocal()

    roles = [
        ("admin", "System administrator"),
        ("manager", "Operations manager"),
        ("engineer", "Support engineer"),
        ("viewer", "Read-only user"),
    ]

    permissions = [
        "create_incident",
        "assign_incident",
        "update_incident",
        "close_incident",
        "view_all",
        "manage_users",
    ]

    role_permissions_map = {
        "admin": permissions,
        "manager": ["create_incident", "assign_incident", "update_incident", "close_incident", "view_all"],
        "engineer": ["update_incident"],
        "viewer": ["view_all"],
    }

    role_objs = {}
    for name, desc in roles:
        role = Role(name=name, description=desc)
        db.add(role)
        db.flush()
        role_objs[name] = role

    perm_objs = {}
    for p in permissions:
        perm = Permission(name=p, description=p.replace("_", " ").title())
        db.add(perm)
        db.flush()
        perm_objs[p] = perm

    for role_name, perms in role_permissions_map.items():
        for p in perms:
            db.add(RolePermission(role_id=role_objs[role_name].id, permission_id=perm_objs[p].id))

    db.commit()
    db.close()

    print("RBAC seeded successfully")

if __name__ == "__main__":
    seed_rbac()
