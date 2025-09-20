from typing import Annotated

from fastapi import APIRouter, Form, Depends, HTTPException, status

from task3.schemas import OrdersGoodsSchema
from task3.dependencies import get_orders_repo
from task3.interfaces import OrdersRepoInterface
from task3 import exc as appexc

orders_router = APIRouter(tags=["orders"])


@orders_router.post(
    '/goods', description='Add goods to order',
    responses={
        200: {'description': 'Goods was added'},
        404: {'description': 'Order or goods with such id does not exist'},
        409: {'description': 'Not enough goods in stock'}
    }
)
async def add_goods_into_order(
        data: Annotated[OrdersGoodsSchema, Form()],
        orders_repo: Annotated[OrdersRepoInterface, Depends(get_orders_repo)]
) -> OrdersGoodsSchema:

    try:
        updated = await orders_repo.add_goods_to_order(data.order_id, data.goods_id, data.amount)
    except (appexc.OrderNotFound, appexc.GoodsNotFound) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{'Order' if isinstance(e, appexc.OrderNotFound) else 'Goods'} not found'
        )
    except appexc.NotEnoughGoodsInStock:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Not enough goods in stock')

    return OrdersGoodsSchema.model_validate(
        dict(order_id=updated.order_id, goods_id=updated.goods_id, amount=updated.amount)
    )