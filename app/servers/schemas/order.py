from pydantic import BaseModel, Field
import uuid

class OrderCreateRequest(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    completed: bool
    date: str

class OrderCreateResponse(BaseModel):
    notificationType: str
    order: OrderCreateRequest
