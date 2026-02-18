from app.models.rbac import UserRole, Role, RolePermission, Permission
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database.database import get_db
from app.models.users import User
import hashlib
from app.core.permissions import get_user_permissions

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "supersecretkey"   # later move to env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha)

def verify_password(plain: str, hashed: str) -> bool:
    sha = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(sha, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # ✅ LOAD USER WITH ROLES + PERMISSIONS IN ONE QUERY
    user = (
        db.query(User)
        .options(
            joinedload(User.user_roles)
            .joinedload(UserRole.role)
            .joinedload(Role.role_permissions)
            .joinedload(RolePermission.permission)
        )
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise credentials_exception

    # ✅ Build permission list dynamically
    permissions = set()

    for ur in user.user_roles:
        for rp in ur.role.role_permissions:
            permissions.add(rp.permission.name)

    user.permissions = list(permissions)

    return user

def require_permission(permission: str):
    def checker(current_user: User = Depends(get_current_user)):
        if permission not in getattr(current_user, "permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return current_user
    return checker
