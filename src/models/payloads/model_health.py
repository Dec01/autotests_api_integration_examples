from pydantic import Field, ValidationError, BaseModel, field_validator
from src.models.processings.response_processing import PydanticResponseError


class Pim(BaseModel):
    service: str

class HealthService(BaseModel):
    status: str = Field(...)
    warnings: object = Field(...)

    @field_validator('status')
    @classmethod
    def force_x_positive_01(cls, v):
        assert v == 'alive'
        return v

    @field_validator('warnings')
    @classmethod
    def force_x_positive_02(cls, v):
        assert v == []
        return v

class SHOPDate(BaseModel):
    healthCheck: bool = Field(...)

    @field_validator('healthCheck')
    @classmethod
    def force_x_positive_02(cls, v):
        assert v == True
        return v

class Shop(BaseModel):
    data: SHOPDate

class Kafka(BaseModel):
    service: str


health_model = {
    'Pim': Pim,
    'CatalogService': HealthService,
    'BFFService': HealthService,
    'Shop': Shop,
    'Kafka': Kafka
}

class ResponsesCheck:

    @staticmethod
    def request_health_check_shop():
        request = """
             query {
               health
             }
        """
        try:
            return request
        except ValidationError as e:
            PydanticResponseError.print_error(e)

    @staticmethod
    def response_health_check(domain_path, data):
        for value, key in health_model.items():
            if value == domain_path:
                try:
                    return key.model_validate(data)
                except ValidationError as e:
                    PydanticResponseError.print_error(e)

