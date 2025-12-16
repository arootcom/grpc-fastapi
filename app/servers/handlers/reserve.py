from loguru import logger

class ReserveHandler:
    @staticmethod
    async def reserve_item(request):
        reserve = { 
            "uuid": request.uuid,
            "name": "asdf",
            "instock": 3,
            "reserve": request.quantity,
        }
        logger.success(f'Reserved item: {reserve}')
        return reserve
