from typing import Protocol

from task3.dbmodels import OrdersGoodsModel


class OrdersRepoInterface(Protocol):

    async def add_goods_to_order(self, order_id: int, goods_id: int, amount: int) -> OrdersGoodsModel:
        ...