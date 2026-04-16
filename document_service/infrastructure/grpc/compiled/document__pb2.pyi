from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class DocumentRecognitionRequest(_message.Message):
    __slots__ = ("image_base64",)
    IMAGE_BASE64_FIELD_NUMBER: _ClassVar[int]
    image_base64: str
    def __init__(self, image_base64: _Optional[str] = ...) -> None: ...

class DocumentRecognitionResponse(_message.Message):
    __slots__ = ("raw",)
    RAW_FIELD_NUMBER: _ClassVar[int]
    raw: str
    def __init__(self, raw: _Optional[str] = ...) -> None: ...
