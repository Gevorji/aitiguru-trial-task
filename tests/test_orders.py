import random

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload


from task3.dbmodels import OrdersGoodsModel, ClientModel, OrderModel, GoodsModel

pytestmark = pytest.mark.anyio


ENDPOINT = f'/orders/goods'


@pytest.fixture(scope='module')
def get_random_entity(async_session_factory):

    async def _get_random_entity(entity_cls, *, options: tuple = tuple()):
        async with async_session_factory() as session:
            return await session.scalar(
                select(entity_cls)
                .order_by(func.random()).limit(1)
                .options(*options)
            )

    return _get_random_entity


async def test_insert_existing_order_goods_successful(
        get_random_entity, test_client, async_session_factory
):

    og = await get_random_entity(OrdersGoodsModel, options=(joinedload(OrdersGoodsModel.goods),))
    stock_amount = og.goods.stock_amount
    additional_amount = random.randint(1, stock_amount - 1)

    response = await test_client.post(
        ENDPOINT, data=dict(order_id=og.order_id, goods_id=og.goods_id, amount=additional_amount),
    )

    assert response.status_code == 200

    async with async_session_factory() as session:
        new_og = await session.get(
            OrdersGoodsModel, (og.order_id, og.goods_id), options=(joinedload(OrdersGoodsModel.goods),)
        )

    assert new_og.goods.stock_amount == stock_amount - additional_amount
    assert new_og.amount == og.amount + additional_amount


async def test_insert_new_order_goods_successful(
    get_random_entity, test_client, async_session_factory
):
    client = await get_random_entity(ClientModel)
    goods = await get_random_entity(GoodsModel)
    stock_amount = goods.stock_amount
    amount = random.randint(1, goods.stock_amount - 1)

    async with async_session_factory() as session, session.begin():
        order = OrderModel(client_id=client.id_, status='created')
        session.add(order)

    response = await test_client.post(
        ENDPOINT, data=dict(order_id=order.id_, goods_id=goods.id_, amount=amount),
    )
    resp_data = response.json()

    assert response.status_code == 200


    async with async_session_factory() as session:
        new_og = await session.get(
            OrdersGoodsModel, (resp_data['order_id'], resp_data['goods_id']),
            options=(joinedload(OrdersGoodsModel.goods),)
        )

    assert new_og is not None
    assert new_og.goods.stock_amount == stock_amount - amount
    assert new_og.amount == amount


async def test_insert_new_order_fail_when_order_amount_more_than_stock(
    get_random_entity, test_client, async_session_factory
):
    client = await get_random_entity(ClientModel)
    goods = await get_random_entity(GoodsModel)
    stock_amount = goods.stock_amount
    amount = goods.stock_amount + 1

    async with async_session_factory() as session:
        orders_goods_count = await session.scalar(select(func.count('*')).select_from(OrdersGoodsModel))

    async with async_session_factory() as session, session.begin():
        order = OrderModel(client_id=client.id_, status='created')
        session.add(order)

    response = await test_client.post(
        ENDPOINT, data=dict(order_id=order.id_, goods_id=goods.id_, amount=amount),
    )

    assert response.status_code == 409

    async with async_session_factory() as session:
        new_goods_amount = await session.scalar(select(GoodsModel.stock_amount).where(GoodsModel.id_ == goods.id_))
        new_orders_goods_count = await session.scalar(select(func.count('*')).select_from(OrdersGoodsModel))

    assert new_goods_amount == stock_amount
    assert new_orders_goods_count == orders_goods_count


async def test_insert_new_order_fail_when_order_does_not_exist(
    get_random_entity, test_client, async_session_factory
):
    goods = await get_random_entity(GoodsModel)


    response = await test_client.post(
        ENDPOINT, data=dict(order_id=100_000, goods_id=goods.id_, amount=random.randint(1, goods.stock_amount - 1)),
    )

    assert response.status_code == 404

    async with async_session_factory() as session:
        new_goods_amount = await session.scalar(select(GoodsModel.stock_amount).where(GoodsModel.id_ == goods.id_))

    assert new_goods_amount == goods.stock_amount


async def test_insert_new_order_fail_when_goods_does_not_exist(
        get_random_entity, test_client, async_session_factory
):
    order = await get_random_entity(OrderModel)

    async with async_session_factory() as session:
        orders_goods_count = await session.scalar(select(func.count('*')).select_from(OrdersGoodsModel))

    response = await test_client.post(
        ENDPOINT, data=dict(order_id=order.id_, goods_id=100_000, amount=random.randint(1, 5)),
    )

    assert response.status_code == 404

    async with async_session_factory() as session:
        new_orders_goods_count = await session.scalar(select(func.count('*')).select_from(OrdersGoodsModel))

    assert new_orders_goods_count == orders_goods_count
