import os
import grpc
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from grpc import aio
from protos.order import order_pb2_grpc
from servers.services.order import OrderService
from models.order import Order

class Server:
    """
    Singleton класс для настройки и запуска gRPC сервера.

    Класс обеспечивает создание единственного экземпляра сервера, который можно зарегистрировать и запустить.

    Атрибуты:
    ---------
    _instance : Server
        Приватный атрибут, содержащий единственный экземпляр класса Server.
    SERVER_ADDRESS : str
        Адрес сервера в формате 'host:port'.
    server : grpc.aio.Server
        Экземпляр асинхронного gRPC сервера.
    initialized : bool
        Флаг, указывающий, была ли выполнена инициализация.

    Методы:
    -------
    __new__(cls, *args, **kwargs)
        Создает и возвращает единственный экземпляр класса Server.
    __init__() -> None
        Инициализирует сервер, если он еще не инициализирован.
    register() -> None
        Регистрирует сервисы gRPC на сервере.
    async run() -> None
        Запускает сервер и ожидает его завершения.
    async stop() -> None
        Останавливает сервер.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Создает и возвращает единственный экземпляр класса Server.

        Если экземпляр уже существует, возвращает его. В противном случае создает новый экземпляр.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Инициализирует сервер, если он еще не инициализирован.

        Устанавливает адрес сервера, создает сервер gRPC и добавляет незащищенный порт.
        """
        if not hasattr(self, 'initialized'):
            self.SERVER_ADDRESS = f'{os.environ["GRPC_HOST_LOCAL"]}:{os.environ["GRPC_PORT"]}'
            self.server = aio.server(ThreadPoolExecutor(max_workers=10))
            self.server.add_insecure_port(self.SERVER_ADDRESS)
            self.initialized = True

    def register(self) -> None:
        """
        Регистрирует сервисы gRPC на сервере.

        Регистрирует сервис OrderService на gRPC сервере.
        """
        order_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderService(), self.server
        )

    async def run(self) -> None:
        """
        Запускает сервер и ожидает его завершения.

        Создает таблицу Order, если она еще не существует, регистрирует сервисы и запускает сервер.
        Логгирует информацию о запуске сервера.
        """
        await Order.create_table(if_not_exists=True)
        self.register()
        await self.server.start()
        logger.info(f'*** Сервис gRPC запущен: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

    async def stop(self) -> None:
        """
        Останавливает сервер.

        Останавливает gRPC сервер без периода ожидания (grace period).
        Логгирует информацию о остановке сервера.
        """
        logger.info('*** Сервис gRPC остановлен ***')
        await self.server.stop(grace=False)
