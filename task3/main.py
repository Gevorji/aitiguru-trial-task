from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import URL

from task3 import dependencies as deps
from task3.repositories import OrdersRepository
from task3.settings import DbConnectionSettings
from task3.routers import orders_router


engine = create_async_engine(
    URL.create(
        drivername=DbConnectionSettings.DRIVER,
        host=DbConnectionSettings.HOST,
        port=DbConnectionSettings.PORT,
        username=DbConnectionSettings.USERNAME,
        password=DbConnectionSettings.PASSWORD,
        database=DbConnectionSettings.DB_NAME,
    )
)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

orders_repo = OrdersRepository(sessionmaker)

deps.set_orders_repository(OrdersRepository)

app = FastAPI()
app.include_router(orders_router, prefix="/orders")
