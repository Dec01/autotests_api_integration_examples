import requests
import configparser
import logging

from dotenv import load_dotenv
from src.models.paths.paths_services import PathsServices

from src.models.payloads.model_shop import PayloadShop

service_domains = PathsServices.service_domains
load_dotenv()

class Requests(object):
    LOGGER = logging.getLogger(__name__)
    parser = configparser.ConfigParser()
    parser.read('pytest.ini')

    @staticmethod
    def get_request(url, method_url, params, headers):
        response = requests.get(url + method_url, params=params, headers=headers, verify=False)
        if response.status_code != 200:
            Requests.LOGGER.info('Request url {}{} with params {}, headers {}'.format(url, method_url, params, headers))
            print('\nResponse StatusCode: {} \n Response body: {}'.format(response.status_code, response.json()))
        return response

    @staticmethod
    def post_request(url, method_url, data, json, headers):
        response = requests.post(url + method_url, data=data,  json=json, headers=headers, verify=True)
        if response.status_code != 200:
            Requests.LOGGER.info('Request url {}{} with data {} , headers {}, body {}'.format(url, method_url, data,
                                                                                              headers, json))
            print('\nResponse StatusCode: {} \n Response body: {}'.format(response.status_code, response.json()))

        return response

    @staticmethod
    def patch_request(url, method_url, data, json, headers):
        response = requests.patch(url + method_url, data=data,  json=json, headers=headers, verify=False)
        if response.status_code != 200:
            Requests.LOGGER.info(
                'Request url {}{} with data {} , headers {}, body {}'.format(url, method_url, data, headers, json))
            print('\nResponse StatusCode: {} \n Response body: {}'.format(response.status_code, response.json()))

        return response

    @staticmethod
    def put_request(url, method_url, data, json, headers):
        response = requests.put(url + method_url, data=data, json=json, headers=headers, verify=False)
        if response.status_code != 200:
            Requests.LOGGER.info('Request url {}{} with data {} , headers {}'.format(url, method_url, data, headers))
            print('\nResponse StatusCode: {} \n Response body: {}'.format(response.status_code, response.json()))

        return response


    @staticmethod
    def delete_request(url, method_url, headers):
        response = requests.delete(url + method_url, headers=headers, verify=False)
        if response.status_code != 200:
            Requests.LOGGER.info('Request url {}{} with headers {}'.format(url, method_url, headers))
            print('\nResponse StatusCode: {} \n Response body: {}'.format(response.status_code, response.json()))

        return response


class Domain(object):
    LOGGER = logging.getLogger(__name__)
    parser = configparser.ConfigParser()
    parser.read('pytest.ini')

    @staticmethod
    def service_domain_definition(domain_name):
        for value, key in service_domains.items():
            if domain_name == value:
                return key
            else:
                pass


class Shop:

    @staticmethod
    def test_generation_token_shop():
        domain_path = PathsServices.service_domains.get("Shop")
        method_path = PathsServices.service_majento_paths.get('ShopServiceStage').get('Token')
        payload = PayloadShop.request_generation_token()
        response = requests.post(domain_path + method_path, json=payload)
        data = response.json()
        return data
