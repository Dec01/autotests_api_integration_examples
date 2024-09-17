import os

from pydantic import Field, ValidationError, BaseModel
from dotenv import load_dotenv
from src.models.processings.response_processing import PydanticResponseError

load_dotenv()


class ShopRequestAuth(BaseModel):
    username: str = Field(...)
    password: str = Field(...)




class PayloadShop:

    @staticmethod
    def request_generation_token():
        payload = ShopRequestAuth(
            username=os.getenv("SHOP_USERNAME"),
            password=os.getenv("SHOP_PASSWORD")
        )
        return_payload = payload.model_dump(mode='json')
        try:
            return return_payload
        except ValidationError as e:
            PydanticResponseError.print_error(e)
