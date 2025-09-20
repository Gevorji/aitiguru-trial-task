import sqlalchemy
from sqlalchemy import update
from sqlalchemy import exc as sqlaexc

from task3.dbmodels import ClientModel, GoodsModel, OrderModel, OrdersGoodsModel, CategoriesModel
from task3.interfaces import OrdersRepoInterface
from task3 import exc as appexc

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class OrdersRepository(OrdersRepoInterface):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):

        self._session_factory = session_factory


    async def add_goods_to_order(self, order_id: int, goods_id: int, amount: int) -> OrdersGoodsModel:

        async with self._session_factory() as session, session.begin():

            try:
                updated_goods = await session.execute(
                    update(GoodsModel)
                    .where(GoodsModel.id_ == goods_id)
                    .values(dict(stock_amount=GoodsModel.stock_amount - amount))
                    .returning(GoodsModel.id_)
                )

                if not updated_goods:
                    raise appexc.GoodsNotFound

            except sqlaexc.IntegrityError:
                raise appexc.NotEnoughGoodsInStock(f'Not enough amount in stock for goods with {goods_id}')

            try:
                nested_tx = await session.begin_nested()
                order_goods_association = OrdersGoodsModel(order_id=order_id, goods_id=goods_id, amount=amount)
                session.add(order_goods_association)
                await nested_tx.commit()
                return order_goods_association
            except sqlaexc.IntegrityError:
                    await nested_tx.rollback()
                    updated_order_goods = await session.scalar(
                        update(OrdersGoodsModel)
                        .where(OrdersGoodsModel.order_id == order_id, OrdersGoodsModel.goods_id == goods_id)
                        .values(dict(amount=OrdersGoodsModel.amount + amount))
                        .returning(OrdersGoodsModel)
                    )

                    if updated_order_goods is None:
                        raise appexc.OrderNotFound

                    return updated_order_goods

