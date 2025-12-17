from pydantic import BaseModel, Field
import uuid
from enum import Enum

class LoyaltyNotificationEnum(Enum):
    LOYALTY_NOTIFICATION_TYPE_ENUM_UNSPECIFIED = 'LOYALTY_NOTIFICATION_TYPE_ENUM_UNSPECIFIED'
    LOYALTY_NOTIFICATION_TYPE_ENUM_OK = 'LOYALTY_NOTIFICATION_TYPE_ENUM_OK'

class Loyalty(BaseModel):
    uuid: str
    persent: int

class LoyaltyRequest(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quantity: int

class LoyaltyResponse(BaseModel):
    notificationType: str = LoyaltyNotificationEnum.LOYALTY_NOTIFICATION_TYPE_ENUM_OK.value
    loyalty: Loyalty
