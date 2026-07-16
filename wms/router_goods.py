from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from tortoise.expressions import Q
from model import Goods

router = APIRouter()


@router.get("/")
async def index():
    return {"message": "Hello, Goods!"}


@router.get("/goods/")
async def get_goods(
    warehouse_id: int = Query(None, description="仓库ID"),
    warehouse_name: str = Query(None, description="仓库名称"),
    min_quantity: int = Query(None, description="最小数量"),
    keyword: str = Query(None, description="搜索关键词"),
):

    query = Goods.all()
    if warehouse_id:
        query = query.filter(warehouse_id=warehouse_id)
    if warehouse_name:
        query = query.filter(warehouse__name__icontains=warehouse_name)
    if min_quantity:
        query = query.filter(quantity__gt=min_quantity)
    if keyword:
        query = query.filter(name__icontains=keyword)
    goods = await query
    return goods


@router.get("/goods/phone")
async def get_goods_phone():
    # prefetch_related()方法可以预加载相关的仓库信息
    goods_list = (
        await Goods.filter(Q(name__icontains="手机") & Q(quantity__gte=1000))
        .prefetch_related("warehouse")
        .all()
    )
    print(goods_list)
    result = []
    for goods in goods_list:
        result.append(
            {
                "id": goods.id,
                "name": goods.name,
                "quantity": goods.quantity,
                "warehouse": {"id": goods.warehouse.id, "name": goods.warehouse.name},
            }
        )

    return result


class GoodsCreate(BaseModel):
    name: str
    warehouse_id: int
    quantity: int = Field(gt=0, description="数量必须大于0")


# 创建新产品
@router.post("/goodsCreate/")
async def create_goods(goods: GoodsCreate):
    goods_obj = await Goods.create(
        name=goods.name,
        warehouse_id=goods.warehouse_id,
        quantity=goods.quantity,
    )
    return goods_obj


# 删除产品
@router.delete("/goods/{goods_id}/")
async def delete_goods(goods_id: int):
    try:
        goods = await Goods.get(id=goods_id)
        await goods.delete()
        return {"message": "Goods deleted successfully"}
    except Goods.DoesNotExist:
        return {"message": "Goods not found"}
