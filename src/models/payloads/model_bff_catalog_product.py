import random

from pydantic import Field, ValidationError, BaseModel, field_validator
from typing import List, Optional
from src.models.processings.response_processing import PydanticResponseError


class BffCatalogProductRequestPaginationList(BaseModel):
    limit: int = Field(...)
    offset: int = Field(...)

class BffCatalogProductRequest(BaseModel):
    pagination: BffCatalogProductRequestPaginationList

class BffCatalogProductResponsePayloadMetaCount(BaseModel):
    count: int = Field(..., gt=1000, lt=15000)

class BffCatalogProductResponsePayloadItemsPricePriceStructureSalePrice(BaseModel):
    price: Optional[float]
    dateActiveFrom: str = Field(...)
    dateActiveTo: str = Field(...)


class BffCatalogProductResponsePayloadItemsPrice(BaseModel):
    basePrice: Optional[int]
    sku: Optional[str]
    salePrice: List[BffCatalogProductResponsePayloadItemsPricePriceStructureSalePrice]




class BffCatalogProductResponsePayloadItemsStock(BaseModel):
    isInStock: Optional[bool]
    sku: Optional[str]


class BffCatalogProductResponsePayloadItems(BaseModel):
    id: str = Field(...)
    code: str = Field(...)
    productFormat: str = Field(...)
    authors: str = Field(...)
    price: BffCatalogProductResponsePayloadItemsPrice
    stock: BffCatalogProductResponsePayloadItemsStock
class BffCatalogProductResponsePayload(BaseModel):
    meta: BffCatalogProductResponsePayloadMetaCount
    items: List[BffCatalogProductResponsePayloadItems]

class BffCatalogProductResponse(BaseModel):
    code: str = Field(...)
    payload: BffCatalogProductResponsePayload
    message: str = Field(...)

    @field_validator('code')
    @classmethod
    def positive_01(cls, v):
        assert v == '0'
        return v

    @field_validator('message')
    @classmethod
    def positive_02(cls, v):
        assert v == 'Success'
        return v


class PayloadBffCatalogProduct:
    @staticmethod
    def request_generation():
        payload = BffCatalogProductRequest(
                pagination=BffCatalogProductRequestPaginationList(
                limit=1,
                offset=random.randint(1, 4000)
            )
          )
        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)

    @staticmethod
    def response_validate(data):
        try:
            return BffCatalogProductResponse.model_validate(data)
        except ValidationError as e:
            PydanticResponseError.print_error(e)



