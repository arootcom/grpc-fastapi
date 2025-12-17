from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoyaltyNotificationTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOYALTY_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: _ClassVar[LoyaltyNotificationTypeEnum]
    LOYALTY_NOTIFICATION_TYPE_ENUM_OK: _ClassVar[LoyaltyNotificationTypeEnum]
LOYALTY_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: LoyaltyNotificationTypeEnum
LOYALTY_NOTIFICATION_TYPE_ENUM_OK: LoyaltyNotificationTypeEnum

class Loyalty(_message.Message):
    __slots__ = ("uuid", "persent")
    UUID_FIELD_NUMBER: _ClassVar[int]
    PERSENT_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    persent: int
    def __init__(self, uuid: _Optional[str] = ..., persent: _Optional[int] = ...) -> None: ...

class LoyaltyRequest(_message.Message):
    __slots__ = ("uuid", "quantity")
    UUID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    quantity: int
    def __init__(self, uuid: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class LoyaltyResponse(_message.Message):
    __slots__ = ("notificationType", "loyalty")
    NOTIFICATIONTYPE_FIELD_NUMBER: _ClassVar[int]
    LOYALTY_FIELD_NUMBER: _ClassVar[int]
    notificationType: LoyaltyNotificationTypeEnum
    loyalty: Loyalty
    def __init__(self, notificationType: _Optional[_Union[LoyaltyNotificationTypeEnum, str]] = ..., loyalty: _Optional[_Union[Loyalty, _Mapping]] = ...) -> None: ...
