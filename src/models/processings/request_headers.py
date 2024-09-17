import os
from dotenv import load_dotenv
from src.models.processings.request_processing import Shop

load_dotenv()

class RequestAuth:
    pim = {'Authorization': f'Bearer {os.getenv("PIM_TOKEN")}'}
    majento_func = Shop.test_generation_token_shop()
    print(majento_func)
    majento = {'Authorization': f'Bearer {majento_func}'}



