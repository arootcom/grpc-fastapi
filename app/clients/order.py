import os
import grpc
from protos.order import order_pb2_grpc

async def grpc_order_client():
    """
    Создает асинхронный gRPC клиент для сервиса OrderService.

    Эта функция создает незащищенный gRPC канал с сервером, используя параметры хоста и порта,
    указанные в настройках, и возвращает клиентский объект для взаимодействия с OrderService.

    Возвращает:
    -----------
    order_pb2_grpc.OrderServiceStub
        Клиентский объект для взаимодействия с gRPC сервисом OrderService.
    """
    channel = grpc.aio.insecure_channel(f'{os.environ["GRPC_HOST_LOCAL"]}:{os.environ["GRPC_PORT"]}')
    client = order_pb2_grpc.OrderServiceStub(channel)
    return client
