from pydantic import Field, ValidationError, BaseModel, field_validator
from src.models.processings.response_processing import PydanticResponseError

class PimResponePost(BaseModel):
    status: str = Field(...)

    @field_validator('status')
    @classmethod
    def force_x_positive_01(cls, v):
        assert v == 'started'
        return v


class UnpublicProductPost(BaseModel):
    product: str = Field(...)
    channel: str = Field(...)

class PayloadPim:

    @staticmethod
    def request_generation(product_id):
        payload = UnpublicProductPost(
            product=product_id,
            channel='kafka'
        )
        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)


    @staticmethod
    def response_validate(data):
        try:
            return PimResponePost.model_validate(data)
        except ValidationError as e:
            PydanticResponseError.print_error(e)



