from tortoise import fields
from tortoise.models import Model


class Warehouse(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "warehouse"


class Goods(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    warehouse = fields.ForeignKeyField("models.Warehouse", related_name="goods")
    quantity = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "goods"
