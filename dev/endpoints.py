from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from db_init import redis_client, users_db
from models import Role, Token, UserResponse
from oauth import Oauth, oauth2_scheme

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(
        username: str = Form(...),
        password: str = Form(...),
        role: Role = Form(..., description="Выберите одну из предопределённых ролей: admin или user", example="admin")
):
    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = Oauth.get_password_hash(password)
    users_db[username] = {"password": hashed_password, "role": role}
    return {"username": username, "role": role}


@router.post("/login", response_model=Token)
def login_user(
        username: str = Form(...),
        password: str = Form(...),
):
    user = users_db.get(username)
    if not user or not Oauth.verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Oauth.create_access_token({"sub": username}, access_token_expires)
    redis_client.setex(access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60, username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user(token: str = Depends(oauth2_scheme)):
    redis_client.sadd("blacklist", token)
    redis_client.delete(token)
    return {"message": "Successfully logged out"}


@router.get("/users", response_model=list[UserResponse])
def get_all_users(current_user: dict = Depends(Oauth.get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return [{"username": u, "role": data["role"]} for u, data in users_db.items()]

