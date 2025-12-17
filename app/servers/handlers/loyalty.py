from loguru import logger

class LoyaltyHandler:
    @staticmethod
    async def loyalty_info(request):
        loyalty = { 
            "uuid": request.uuid,
            "persent": 10,
        }
        logger.success(f'Loyalty info: {loyalty}')
        return loyalty
