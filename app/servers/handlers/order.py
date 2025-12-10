from models.order import Order

class OrderHandler:
    @staticmethod
    async def create_order(request):
        order = Order(**request.dict())
        await order.save()
        return order
