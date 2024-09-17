from pydantic import Field, ValidationError, BaseModel, field_validator
from src.models.processings.response_processing import PydanticResponseError
from faker import Faker

fake = Faker(locale="ru_RU")


class RequestBffPostCatalogProduct(BaseModel):
    category: str = Field(...)
    query: str = Field(...)

class ResponseBffPostCatalogProduct(BaseModel):
    status: str = Field(...)

    @field_validator('status')
    @classmethod
    def force_x_positive_01(cls, v):
        assert v == 'start'
        return v

class PayloadBffPostCatalogProduct:

    @staticmethod
    def request_generation(category, query):
        payload = RequestBffPostCatalogProduct(
            category=category,
            query=query
        )
        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)


    @staticmethod
    def response_validate(data):
        try:
            return ResponseBffPostCatalogProduct.model_validate(data)
        except ValidationError as e:
            PydanticResponseError.print_error(e)



