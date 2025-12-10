from models.order import Order
from loguru import logger

class OrderHandler:
    @staticmethod
    async def create_order(request):
        order = await Order.insert(Order(**request.dict()))
        logger.success(f'Created order: {order}')
        return order
