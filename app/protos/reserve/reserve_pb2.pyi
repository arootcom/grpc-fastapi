from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReserveNotificationTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RESERVE_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: _ClassVar[ReserveNotificationTypeEnum]
    RESERVE_NOTIFICATION_TYPE_ENUM_OK: _ClassVar[ReserveNotificationTypeEnum]
RESERVE_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: ReserveNotificationTypeEnum
RESERVE_NOTIFICATION_TYPE_ENUM_OK: ReserveNotificationTypeEnum

class Item(_message.Message):
    __slots__ = ("uuid", "name", "instock", "reserve")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INSTOCK_FIELD_NUMBER: _ClassVar[int]
    RESERVE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    instock: int
    reserve: int
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., instock: _Optional[int] = ..., reserve: _Optional[int] = ...) -> None: ...

class ReserveItemRequest(_message.Message):
    __slots__ = ("uuid", "quantity")
    UUID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    quantity: int
    def __init__(self, uuid: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class ReserveItemResponse(_message.Message):
    __slots__ = ("notificationType", "item")
    NOTIFICATIONTYPE_FIELD_NUMBER: _ClassVar[int]
    ITEM_FIELD_NUMBER: _ClassVar[int]
    notificationType: ReserveNotificationTypeEnum
    item: Item
    def __init__(self, notificationType: _Optional[_Union[ReserveNotificationTypeEnum, str]] = ..., item: _Optional[_Union[Item, _Mapping]] = ...) -> None: ...
