from datetime import datetime

from fastapi import APIRouter

from model import Warehouse

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello, Warehouse!"}


# 获取所有仓库
@router.get("/warehouses/")
async def get_warehouse():
    warehouse = await Warehouse.all()
    return warehouse


# 创建仓库
@router.post("/warehouses/")
async def create_warehouse(name: str):
    warehouse = await Warehouse.create(name=name, created_at=datetime.now())
    return warehouse


# 删除仓库
@router.delete("/warehouses/{warehouse_id}/")
async def delete_warehouse(warehouse_id: int):
    warehouse = await Warehouse.get_or_none(id=warehouse_id)
    if warehouse:
        await warehouse.delete()
        return {"message": "Warehouse deleted successfully"}
    else:
        return {"message": "Warehouse not found"}
