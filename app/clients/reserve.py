import os
import grpc
from protos.reserve import reserve_pb2_grpc

async def grpc_reserve_client():
    channel = grpc.aio.insecure_channel(f'{os.environ["GRPC_HOST_RESERVE"]}:{os.environ["GRPC_PORT"]}')
    client = reserve_pb2_grpc.ReserveServiceStub(channel)
    return client
