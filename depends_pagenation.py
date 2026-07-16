from fastapi import FastAPI, Depends, Query
import uvicorn


def pagination(page: int = Query(1, ge=1), size: int = Query(10, gt=1, le=100)):
    return {"page": page, "size": size}


app = FastAPI()


@app.get("/items/")
async def read_items(pagination: dict = Depends(pagination)):
    return {"pagination": pagination, "items": ["item1", "item2", "item3"]}


@app.get("/users/")
async def read_users(pagination: dict = Depends(pagination)):
    return {"pagination": pagination, "users": ["user1", "user2", "user3"]}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
