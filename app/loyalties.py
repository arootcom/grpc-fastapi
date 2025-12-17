import grpc
import asyncio
from servers.loyalties import Server

async def serve() -> None:
    await Server().run()
    await Server().stop()

if __name__ == "__main__":
    asyncio.run(serve())
