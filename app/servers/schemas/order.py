from pydantic import BaseModel, Field
import uuid
from enum import Enum

class OrderNotificationEnum(Enum):
    ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED = 'ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED'
    ORDER_NOTIFICATION_TYPE_ENUM_OK = 'ORDER_NOTIFICATION_TYPE_ENUM_OK'

class OrderResponse(BaseModel):
    uuid: str
    name: str = None
    completed: bool = False
    date: str = None

class OrderCreateRequest(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    completed: bool
    date: str

class OrderCreateResponse(BaseModel):
    notificationType: str = OrderNotificationEnum.ORDER_NOTIFICATION_TYPE_ENUM_OK.value
    order: OrderResponse
