import typing as t
import jwt
from datetime import datetime, timedelta
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from grpc.aio import AioRpcError
from google.protobuf.json_format import MessageToDict

from protos.order import order_pb2
from clients.order import grpc_order_client

router = APIRouter(prefix='/order', tags=['Order'])

@router.get("/{uuid:str}")
async def single_order(
        uuid: str,
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    """
    Получает данные одного заказа по UUID через gRPC сервис OrderService.

    Функция вызывает метод ReadOrder gRPC сервиса OrderService для получения данных заказа по указанному UUID.
    В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    uuid : str
        Уникальный идентификатор заказа.
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными запрошенного заказа.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
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
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    """
    Создает новый заказ через gRPC сервис OrderService.

    Функция вызывает метод CreateOrder gRPC сервиса OrderService для создания нового заказа
    с указанными параметрами. В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    name : str
        Название заказа.
    completed : bool
        Статус выполнения заказа.
    date : str, optional
        Дата создания заказа в формате строки (по умолчанию текущая дата и время в формате UTC с 'Z').
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными созданного заказа.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
    try:
        order = await client.CreateOrder(
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


