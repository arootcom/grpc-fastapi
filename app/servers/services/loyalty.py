from loguru import logger

from protos.loyalty import loyalty_pb2
from protos.loyalty import loyalty_pb2_grpc
from servers.schemas.loyalty import LoyaltyRequest, LoyaltyResponse, Loyalty
from servers.handlers.loyalty import LoyaltyHandler
from servers.utils import GrpcParseMessage

class LoyaltyService(loyalty_pb2_grpc.LoyaltyServiceServicer):

    def __init__(self) -> None:
        self.message = GrpcParseMessage()

    async def LoyaltyInfo(self, request, context) -> loyalty_pb2.LoyaltyResponse:
        request = LoyaltyRequest(**self.message.rpc_to_dict(request))
        logger.info(f'Received request is for loyalty info: {request}')

        result = await LoyaltyHandler.loyalty_info(request=request)
        result = LoyaltyResponse(loyalty=Loyalty(**result))
        logger.debug(f'Result loyalty info: {result}')

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=loyalty_pb2.LoyaltyResponse(),
        )
        return response
