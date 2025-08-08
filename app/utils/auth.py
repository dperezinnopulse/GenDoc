import os
from itsdangerous import URLSafeSerializer, BadSignature
from fastapi import Cookie, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv

load_dotenv("/workspace/pdfgen/.env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

serializer = URLSafeSerializer(SECRET_KEY, salt="session")

SESSION_COOKIE_NAME = "pdfgen_session"


def get_session_user(session: str | None = Cookie(default=None, name=SESSION_COOKIE_NAME)) -> str | None:
    if not session:
        return None
    try:
        data = serializer.loads(session)
        return data.get("user")
    except BadSignature:
        return None


def make_session_token(username: str) -> str:
    return serializer.dumps({"user": username})


def set_auth_cookie(response: Response, token: str):
    response.set_cookie(SESSION_COOKIE_NAME, token, httponly=True, samesite="lax")


def clear_auth_cookie(response: Response):
    response.delete_cookie(SESSION_COOKIE_NAME)


def login_user(username: str, password: str) -> str | None:
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return make_session_token(username)
    return None


def require_user(user: str | None = None, session: str | None = Cookie(default=None, name=SESSION_COOKIE_NAME)) -> str:
    user = get_session_user(session)
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user


def logout_user():
    # Caller will handle Redirect; here we only craft a response with cookie cleared if needed in future
    return True