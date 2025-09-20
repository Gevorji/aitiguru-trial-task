import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncConnection
from sqlalchemy import text
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport


from task3 import dependencies as deps
from task3.repositories import OrdersRepository
from task3.routers import orders_router
from task3.dbmodels import BaseORMModel

POSTGRES_IMAGE = 'postgres:17'


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
async def postgres_container():
    postgres = PostgresContainer(POSTGRES_IMAGE)
    try:
        postgres.start()
        yield postgres
    finally:
        postgres.stop()


@pytest.fixture(scope='session')
async def sqla_engine(postgres_container: PostgresContainer):
    url = postgres_container.get_connection_url(driver='asyncpg')
    engine = create_async_engine(url)

    return engine

@pytest.fixture(scope='session')
async def create_schema(sqla_engine: AsyncEngine):
    meta = BaseORMModel.metadata
    async with sqla_engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


@pytest.fixture(scope='session')
async def insert_test_data(create_schema, sqla_engine):
    insert_categories = open('tests/insert_categories.sql').read()
    insert_test_data = open('tests/test_data_fill_in.sql').read()

    stmts = [text(stmt) for stmt in insert_categories.split(';')] + [text(stmt) for stmt in  insert_test_data.split(';')]

    async with sqla_engine.begin() as conn:
        for stmt in stmts:
            await conn.execute(stmt)


@pytest.fixture(scope="session")
async def db_connection(insert_test_data, sqla_engine) -> AsyncConnection:
    connection = await sqla_engine.connect()
    yield connection
    await connection.close()


@pytest.fixture(scope='session')
async def async_session_factory(db_connection):

    sessionmaker = async_sessionmaker(
        bind=db_connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    return sessionmaker


@pytest.fixture(autouse=True)
async def rollback_changes_made_to_db(
    db_connection,
):  # changes made during each test are rolled back
    transaction = await db_connection.begin()
    yield
    await transaction.rollback()


@pytest.fixture(scope='module')
async def app(async_session_factory):

    orders_repo = OrdersRepository(async_session_factory)
    deps.set_orders_repository(orders_repo)

    fapi = FastAPI()
    fapi.include_router(orders_router, prefix='/orders')

    return fapi


@pytest.fixture
async def test_client(app):

    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://127.0.0.1")

    yield client

    await client.aclose()
