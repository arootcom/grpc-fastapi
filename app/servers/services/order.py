from loguru import logger

from protos.order import order_pb2
from protos.order import order_pb2_grpc
from servers.schemas.order import OrderCreateRequest, OrderCreateResponse, OrderResponse
from servers.handlers.order import OrderHandler
from servers.utils import GrpcParseMessage

class OrderService(order_pb2_grpc.OrderServiceServicer):

    # Инициализация экземпляра OrderService.
    def __init__(self) -> None:
        # Создает объект GrpcParseMessage для преобразования сообщений между
        # форматами gRPC и внутренними форматами данных.
        self.message = GrpcParseMessage()

    # Обрабатывает gRPC запрос на создание заказа.
    # Параметры:
    #   request : order_pb2.CreateOrderRequest - gRPC сообщение с данными для создания заказа.
    #   context : grpc.aio.ServicerContext -Контекст сервиса gRPC, содержащий информацию о текущем RPC.
    # Возвращает:
    #   order_pb2.CreateOrderResponse - gRPC сообщение с результатом операции создания заказа.
    async def CreateOrder(self, request, context) -> order_pb2.CreateOrderResponse:
        request = OrderCreateRequest(**self.message.rpc_to_dict(request))
        logger.info(f'Received request is for create order: {request}')

        result = await OrderHandler.create_order(request=request)
        result = OrderCreateResponse(order=OrderResponse(**result[0]))
        logger.debug(f'Result created order: {result}')

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.CreateOrderResponse(),
        )
        return response
