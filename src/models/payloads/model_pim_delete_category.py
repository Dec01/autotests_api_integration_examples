from pydantic import Field, ValidationError, BaseModel, field_validator
from src.models.processings.response_processing import PydanticResponseError
from faker import Faker

fake = Faker(locale="ru_RU")



class RequestPimDeleteCategory(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    parent: str = Field(...)

class ResponsePimDeleteCategory(BaseModel):
    status: str = Field(...)

    @field_validator('status')
    @classmethod
    def force_x_positive_01(cls, v):
        assert v == 'start'
        return v



class PayloadPimDeleteCategory:

    @staticmethod
    def request_generation(category_id, category_name):
        payload = RequestPimDeleteCategory(
            id=category_id,
            name=category_name,
            parent='1234567'

        )

        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)


    @staticmethod
    def response_validate(data):
        try:
            return ResponsePimDeleteCategory.model_validate(data)
        except ValidationError as e:
            PydanticResponseError.print_error(e)



