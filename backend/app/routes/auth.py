from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.users import User
from app.core.security import hash_password, verify_password, create_access_token
from app.models.auth import RegisterRequest
from app.core.permissions import get_user_permissions
from sqlalchemy.orm import joinedload
from app.models.rbac import UserRole, Role, RolePermission
from app.models.rbac import UserRole, Role

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    default_role = db.query(Role).filter(Role.name == "viewer").first()

    db.add(UserRole(
        user_id=user.id,
        role_id=default_role.id
    ))
    db.commit()

    return {"message": "User created with viewer role"}

@router.post("/login", summary="Login and get access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .options(
            joinedload(User.user_roles)
            .joinedload(UserRole.role)
            .joinedload(Role.role_permissions)
            .joinedload(RolePermission.permission)
        )
        .filter(User.email == form_data.username)
        .first()
    )

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    
    permissions = get_user_permissions(user)

    token = create_access_token({
        "user_id": user.id,
        "permissions": permissions
    })

    return {"access_token": token, "token_type": "bearer"}