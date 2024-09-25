from fastapi import HTTPException
from app.v1.utils.models import ResponseModel


class CustomHTTPException(HTTPException):
    def __init__(self, response_model: ResponseModel):
        self.response_model = response_model
        super().__init__(status_code=response_model.status_code, detail=response_model.dict())
