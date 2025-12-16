from loguru import logger

from protos.reserve import reserve_pb2
from protos.reserve import reserve_pb2_grpc
from servers.schemas.reserve import ReserveItemRequest, ReserveItemResponse, Item
from servers.handlers.reserve import ReserveHandler
from servers.utils import GrpcParseMessage

class ReserveService(reserve_pb2_grpc.ReserveServiceServicer):

    def __init__(self) -> None:
        self.message = GrpcParseMessage()

    async def ReserveItem(self, request, context) -> reserve_pb2.ReserveItemResponse:
        request = ReserveItemRequest(**self.message.rpc_to_dict(request))
        logger.info(f'Received request is for reserve item: {request}')

        result = await ReserveHandler.reserve_item(request=request)
        result = ReserveItemResponse(item=Item(**result))
        logger.debug(f'Result reserve item: {result}')

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=reserve_pb2.ReserveItemResponse(),
        )
        return response
