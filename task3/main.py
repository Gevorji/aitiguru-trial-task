from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import URL

from task3 import dependencies as deps
from task3.repositories import OrdersRepository
from task3.settings import DbConnectionSettings
from task3.routers import orders_router

db_conn_settings = DbConnectionSettings()

engine = create_async_engine(
    URL.create(
        drivername=f'{db_conn_settings.DBMS}+{db_conn_settings.DRIVER}',
        host=db_conn_settings.HOST,
        port=db_conn_settings.PORT,
        username=db_conn_settings.USERNAME,
        password=db_conn_settings.PASSWORD,
        database=db_conn_settings.DB_NAME,
    )
)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

orders_repo = OrdersRepository(sessionmaker)

deps.set_orders_repository(orders_repo)

app = FastAPI()
app.include_router(orders_router, prefix="/orders")
