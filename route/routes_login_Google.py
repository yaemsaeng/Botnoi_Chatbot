from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from urllib.parse import urlencode
from config.db import collection_account
from functools import wraps

RouterGoogle = APIRouter()

client_secrets_file = "client_secret.json"

GOOGLE_CLIENT_ID = "642643535438-mm2947mq2360qr4429tmcjec7lje530j.apps.googleusercontent.com"
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:8000/google/callback"  # เปลี่ยนเป็น backend url ของคุณ
)

def login_is_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if "google_id" not in request.session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
        return await func(request, *args, **kwargs)
    return wrapper

@RouterGoogle.get("/login")
async def login(request: Request):
    authorization_url, state = flow.authorization_url()
    request.session["state"] = state
    return RedirectResponse(authorization_url)

@RouterGoogle.get("/callback")
async def callback(request: Request):
    flow.fetch_token(authorization_response=str(request.url))

    if not request.session.get("state") == request.query_params.get("state"):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="State does not match!")

    credentials = flow.credentials
    token_request = google.auth.transport.requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    request.session["google_id"] = id_info.get("sub")
    request.session["name"] = id_info.get("name")

    # เก็บข้อมูลผู้ใช้ในฐานข้อมูล ถ้ายังไม่มี
    if collection_account.find_one({"sub": id_info.get("sub")}) is None:
        collection_account.insert_one(id_info)

    # ส่ง redirect ไปหน้า frontend login callback พร้อม query params
    frontend_path = "http://localhost:4200/login/callback"  # เปลี่ยนเป็น URL frontend ของคุณ
    query_params = {
        "google_id": id_info.get("sub"),
        "name": id_info.get("name")
    }
    redirect_url = f"{frontend_path}?" + urlencode(query_params)

    return RedirectResponse(redirect_url)
