from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from route.routes import Router
from route.routes_login_Google import RouterGoogle

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ติดตั้ง SessionMiddleware ที่นี่แค่ที่เดียว
app.add_middleware(SessionMiddleware, secret_key="dVu9jfC1PPVGRkq-X5nKaP_vDHC63CxQ2K4W0QVpFJo")

# รวม router หลัก
app.include_router(Router)

# รวม router google login ด้วย prefix /google
app.include_router(RouterGoogle, prefix="/google")
