from fastapi import APIRouter
import uvicorn
from pydantic import BaseModel


class user(BaseModel):
    name: str
    age: int


router = APIRouter()


@router.get("/", response_model=list[user])
async def all():
    return [{"name": "alice", "age": 22}, {"name": "uu", "age": 33}]
