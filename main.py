from fastapi import FastAPI
from route.routes import Router
from fastapi.middleware.cors import CORSMiddleware
from route.routes_login_Google import app as routes_app
from route.purchase import app as routes_purchase
from config.db import collection  # เชื่อมต่อ MongoDB จากไฟล์ db.py

app = FastAPI()

@app.get("/")
def root():
    doc = collection.find_one({})
    if doc:
        doc["_id"] = str(doc["_id"])  # แปลง ObjectId เป็น string
    return {"data": doc}

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
app.mount("", routes_app)
