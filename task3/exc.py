class AppException(Exception):
    ...


class OrdersException(AppException):
    ...


class GoodsException(AppException):
    ...


class NotEnoughGoodsInStock(OrdersException):
    ...


class GoodsNotFound(GoodsException):
    ...


class OrderNotFound(OrdersException):
    ...