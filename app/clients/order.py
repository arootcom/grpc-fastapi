import os
import grpc
from protos.order import order_pb2_grpc

async def grpc_order_client():
    # Cоздает незащищенный gRPC канал с сервером, используя параметры хоста и порта
    channel = grpc.aio.insecure_channel(f'{os.environ["GRPC_HOST_ORDERS"]}:{os.environ["GRPC_PORT"]}')
    
    # Клиентский объект для взаимодействия с gRPC сервисом OrderService.
    client = order_pb2_grpc.OrderServiceStub(channel)
    
    return client
