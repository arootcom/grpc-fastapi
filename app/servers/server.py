import os
import grpc
from loguru import logger
from grpc import aio
from grpc_reflection.v1alpha import reflection
from concurrent.futures import ThreadPoolExecutor

from protos.order import order_pb2
from protos.order import order_pb2_grpc
from servers.services.order import OrderService
from models.order import Order

from protos.reserve import reserve_pb2
from protos.reserve import reserve_pb2_grpc
from servers.services.reserve import ReserveService

class Server:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.SERVER_ADDRESS = f'{os.environ["GRPC_HOST_LOCAL"]}:{os.environ["GRPC_PORT"]}'
            self.server = aio.server(ThreadPoolExecutor(max_workers=10))
            self.server.add_insecure_port(self.SERVER_ADDRESS)

            SERVICE_NAMES = (
                order_pb2.DESCRIPTOR.services_by_name["OrderService"].full_name,
                reserve_pb2.DESCRIPTOR.services_by_name["ReserveService"].full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self.server)

            self.initialized = True

    def register(self) -> None:
        order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), self.server)
        reserve_pb2_grpc.add_ReserveServiceServicer_to_server(ReserveService(), self.server)

    async def run(self) -> None:
        await Order.create_table(if_not_exists=True)
        self.register()
        await self.server.start()
        logger.info(f'*** Сервис gRPC запущен: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

    async def stop(self) -> None:
        logger.info('*** Сервис gRPC остановлен ***')
        await self.server.stop(grace=False)
