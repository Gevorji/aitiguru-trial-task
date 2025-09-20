import enum
from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import Enum


class BaseORMModel(DeclarativeBase):
    ...


class GoodsModel(AsyncAttrs, BaseORMModel):

    __tablename__ = 'goods'

    id_: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str]
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))
    stock_amount: Mapped[int] = mapped_column(CheckConstraint('stock_amount >= 0'), default=0)
    price_per_unit: Mapped[Decimal]

    category: Mapped['CategoriesModel'] = relationship(back_populates='goods')


class CategoriesModel(AsyncAttrs, BaseORMModel):

    __tablename__ = 'categories'

    id_: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str]
    parent_category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))

    goods: Mapped[list['GoodsModel']] = relationship(back_populates='category')


class ClientModel(AsyncAttrs, BaseORMModel):

    __tablename__ = 'clients'

    id_: Mapped[int] = mapped_column('id', primary_key=True)
    name: Mapped[str]
    address: Mapped[str]

    orders: Mapped[list['OrderModel']] = relationship(back_populates='client')



class OrderModel(AsyncAttrs, BaseORMModel):

    __tablename__ = 'orders'

    id_: Mapped[int] = mapped_column('id', primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id'))
    status = mapped_column(ENUM('created', 'sent', 'delivered', name='order_status'))

    client: Mapped['ClientModel'] = relationship(back_populates='orders')
    goods_associations: Mapped[list['OrdersGoodsModel']] = relationship()


class OrdersGoodsModel(AsyncAttrs, BaseORMModel):

    __tablename__ = 'orders_goods'

    __table_args__ = (PrimaryKeyConstraint('order_id', 'goods_id'),)

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    goods_id: Mapped[int] = mapped_column(ForeignKey('goods.id'))
    amount: Mapped[int] = mapped_column(CheckConstraint('amount > 0'))

    goods: Mapped['GoodsModel'] = relationship()


