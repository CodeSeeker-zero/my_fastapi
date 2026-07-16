from fastapi import APIRouter
from pydantic import BaseModel


class student(BaseModel):
    stdno: int
    name: str


router = APIRouter()


@router.get("/", response_model=list[student])
async def all():
    # return [{"stdno": 1, "name": "alice"}, {"stdno": 2, "name": "bob"}]
    return [student(stdno=1, name="alice"), student(stdno=2, name="ooop")]
