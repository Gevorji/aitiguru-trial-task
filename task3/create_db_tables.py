import asyncio

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from task3.settings import DbConnectionSettings
from task3.dbmodels import BaseORMModel

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


async def create_tables():

    meta = BaseORMModel.metadata
    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


if __name__ == '__main__':

    asyncio.run(create_tables())