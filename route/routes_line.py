from fastapi import APIRouter
from model.models import User
from config.db import collection_line

lineRouter = APIRouter()

@lineRouter.post("/post", tags=["user"])
async def post_users(user: line_user):
    collection_line.insert_one(dict(user))
    return {"status": "OK"}
