from task3.interfaces import OrdersRepoInterface


_orders_repository: OrdersRepoInterface | None = None


def set_orders_repository(repo: OrdersRepoInterface):

    global _orders_repository

    _orders_repository = repo


async def get_orders_repo() -> OrdersRepoInterface | None:

    global _orders_repository

    if _orders_repository is None:
        raise AttributeError('Orders repository is not set')

    return _orders_repository
