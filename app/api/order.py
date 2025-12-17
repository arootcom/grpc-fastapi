import typing as t
import jwt
from datetime import datetime, timedelta
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from grpc.aio import AioRpcError
from google.protobuf.json_format import MessageToDict

from protos.order import order_pb2
from protos.reserve import reserve_pb2
from clients.order import grpc_order_client
from clients.reserve import grpc_reserve_client

router = APIRouter(prefix='/order', tags=['Order'])

@router.get("/{uuid:str}")
async def single_order(
        uuid: str,
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    try:
        order = await client.ReadOrder(order_pb2.ReadOrderRequest(uuid=uuid))
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(OrderReadResponse(**MessageToDict(order)).dict())


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
        name: str,
        completed: bool,
        date: str = f'{datetime.utcnow()}Z',
        client_orders: t.Any = Depends(grpc_order_client),
        client_reserve: t.Any = Depends(grpc_reserve_client),
) -> JSONResponse:
    try:
        reserve = await client_reserve.ReserveItem(
            reserve_pb2.ReserveItemRequest(
                uuid = "5f23a419-3a68-4c6a-87a9-d14f9f021a64",
                quantity = 10,
            )
        )

        order = await client_orders.CreateOrder(
            order_pb2.CreateOrderRequest(
                name=name,
                completed=completed,
                date=date
            )
        )
    except AioRpcError as e:
        logger.error(e.details())
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))


