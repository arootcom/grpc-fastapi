from pydantic import BaseModel, Field
import uuid
from enum import Enum

class ReserveNotificationEnum(Enum):
    RESERVE_NOTIFICATION_TYPE_ENUM_UNSPECIFIED = 'RESERVE_NOTIFICATION_TYPE_ENUM_UNSPECIFIED'
    RESERVE_NOTIFICATION_TYPE_ENUM_OK = 'RESERVE_NOTIFICATION_TYPE_ENUM_OK'

class Item(BaseModel):
    uuid: str
    name: str = None
    instock: int
    reserve: int

class ReserveItemRequest(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quantity: int

class ReserveItemResponse(BaseModel):
    notificationType: str = ReserveNotificationEnum.RESERVE_NOTIFICATION_TYPE_ENUM_OK.value
    item: Item
