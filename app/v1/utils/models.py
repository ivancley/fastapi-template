from typing import Any, List, Optional, Union, TypeVar, Generic
from pydantic.generics import GenericModel
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status_code: int
    system_version: Optional[str] = None
    data: Optional[Any] = None
    errors: Optional[Union[List[str], str]] = None

    model_config = {
        'arbitrary_types_allowed': True
    }