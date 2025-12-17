import os
import grpc
from protos.loyalty import loyalty_pb2_grpc

async def grpc_loyalty_client():
    channel = grpc.aio.insecure_channel(f'{os.environ["GRPC_HOST_LOYALTIES"]}:{os.environ["GRPC_PORT"]}')
    client = loyalty_pb2_grpc.LoyaltyServiceStub(channel)
    return client
