from pydantic import Field, ValidationError, BaseModel, field_validator
from src.models.processings.response_processing import PydanticResponseError
from faker import Faker

fake = Faker(locale="ru_RU")



class RequestPimPostLinkCategoryProduct(BaseModel):
    category: int = Field(...)
    product: int = Field(...)
    type: str = Field(...)
class ResponsePimPostLinkCategoryProduct(BaseModel):
    status: str = Field(...)

    @field_validator('status')
    @classmethod
    def force_x_positive_01(cls, v):
        assert v == 'start'
        return v


class PayloadPimPostLinkCategoryProduct:

    @staticmethod
    def request_generation(category_id, product_id, is_main):
        payload = RequestPimPostLinkCategoryProduct(
            category=category_id,
            product=product_id,
            type='1',

        )

        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)


    @staticmethod
    def response_validate(data):
        try:
            return ResponsePimPostLinkCategoryProduct.model_validate(data)
        except ValidationError as e:
            PydanticResponseError.print_error(e)



