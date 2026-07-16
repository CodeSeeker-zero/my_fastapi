from pydantic import BaseModel
from fastapi import FastAPI

import uvicorn

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: int


@app.post("/item/{item_id}")
def create_item(item_id: int, item: Item):
    """创建或更新 item 使用 POST 因为需要 body"""
    result = {"item_id": item_id}
    if item:
        result.update({"item": item})

    return result


if __name__ == "__main__":
    uvicorn.run(app, port=8888)
