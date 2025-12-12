import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from servers.server import Server
from api import order

app = FastAPI(
    title='API Gateway',
    description='',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order.router)

if __name__ == '__main__':
    uvicorn.run('gw:app', port=int(os.environ["SERVICE_PORT"]), host=f'{os.environ["SERVICE_HOST_LOCAL"]}', log_level="debug", reload=True)
