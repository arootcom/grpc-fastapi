import os
import grpc
from loguru import logger
from grpc import aio
from grpc_reflection.v1alpha import reflection
from concurrent.futures import ThreadPoolExecutor

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
                reserve_pb2.DESCRIPTOR.services_by_name["ReserveService"].full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self.server)
            logger.info(f'Enable reflation server')

            self.initialized = True

    def register(self) -> None:
        reserve_pb2_grpc.add_ReserveServiceServicer_to_server(ReserveService(), self.server)
        logger.info(f'Register: Reserve Service')

    async def run(self) -> None:
        self.register()
        await self.server.start()
        logger.info(f'*** Сервис Reserve gRPC запущен: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

    async def stop(self) -> None:
        logger.info('*** Сервис Reserve gRPC остановлен ***')
        await self.server.stop(grace=False)
