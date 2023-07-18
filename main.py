from fastapi import FastAPI
from route.routes import Router
from route.routes_line import lineRouter
from fastapi.middleware.cors import CORSMiddleware
from route.routes_login_Google import app as routes_app
app = FastAPI()


origins = [
    "http://localhost/",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Router)
app.include_router(lineRouter)
app.mount("", routes_app)
