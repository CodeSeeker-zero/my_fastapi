from fastapi import FastAPI
from router_goods import router as goods_router
from router_warehouse import router as warehouse_router
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from model import Warehouse, Goods

app = FastAPI()

register_tortoise(
    app,
    db_url="mysql://root:123456@localhost:3306/myfastapi",
    modules={"models": ["model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(goods_router, prefix="/goods", tags=["goods"])
app.include_router(warehouse_router, prefix="/warehouse", tags=["warehouse"])


@app.get("/")
async def index():
    return {"message": "Hello, WMS!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
