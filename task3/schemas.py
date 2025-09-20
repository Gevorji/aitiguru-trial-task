from pydantic import BaseModel, PositiveInt


class OrdersGoodsSchema(BaseModel):

    order_id: PositiveInt
    goods_id: PositiveInt
    amount: PositiveInt


