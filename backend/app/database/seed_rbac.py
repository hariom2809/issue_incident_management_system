from app.database.database import SessionLocal
from app.models.rbac import Role, Permission, RolePermission


def seed_rbac():
    db = SessionLocal()

    # --------------------------------------------------
    # ROLES
    # --------------------------------------------------
    roles = [
        ("admin", "System administrator"),
        ("manager", "Operations manager"),
        ("engineer", "Support engineer"),
        ("reporter", "Incident reporter"),
    ]

    # --------------------------------------------------
    # PERMISSIONS (FINAL DESIGN)
    # --------------------------------------------------
    permissions = [
        "create_incident",
        "assign_incident",
        "update_incident",
        "close_incident",
        "delete_own_incident",
        "comment_incident",
        "view_all",
        "view_assigned",
        "view_own",
        "manage_users",
    ]

    # --------------------------------------------------
    # ROLE → PERMISSION MAPPING
    # --------------------------------------------------
    role_permissions_map = {
        # Full access
        "admin": permissions,

        # Operational controller
        "manager": [
            "create_incident",
            "assign_incident",
            "update_incident",
            "close_incident",
            "comment_incident",
            "view_all",
        ],

        # Works on assigned incidents only
        "engineer": [
            "update_incident",
            "comment_incident",
            "view_assigned",
        ],

        # Creates incidents and tracks own tickets
        "reporter": [
            "create_incident",
            "comment_incident",
            "delete_own_incident",
            "view_own",
        ],
    }

    # --------------------------------------------------
    # CREATE ROLES
    # --------------------------------------------------
    role_objs = {}
    for name, desc in roles:
        role = Role(name=name, description=desc)
        db.add(role)
        db.flush()  # get generated ID
        role_objs[name] = role

    # --------------------------------------------------
    # CREATE PERMISSIONS
    # --------------------------------------------------
    perm_objs = {}
    for perm_name in permissions:
        perm = Permission(
            name=perm_name,
            description=perm_name.replace("_", " ").title()
        )
        db.add(perm)
        db.flush()
        perm_objs[perm_name] = perm

    # --------------------------------------------------
    # ASSIGN PERMISSIONS TO ROLES
    # --------------------------------------------------
    for role_name, perms in role_permissions_map.items():
        for perm_name in perms:
            db.add(
                RolePermission(
                    role_id=role_objs[role_name].id,
                    permission_id=perm_objs[perm_name].id
                )
            )

    db.commit()
    db.close()

    print("✅ RBAC seeded successfully")


if __name__ == "__main__":
    seed_rbac()