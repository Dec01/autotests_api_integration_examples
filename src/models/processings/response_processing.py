from src.models.utils.ascii import BColors
import requests
import configparser
import logging
from dotenv import load_dotenv
from src.models.paths.paths_services import PathsServices

service_domains = PathsServices.service_domains
load_dotenv()

class Response(object):
    LOGGER = logging.getLogger(__name__)
    parser = configparser.ConfigParser()
    parser.read('pytest.ini')

    @staticmethod
    def get_request(url, method_url, params, headers):
        response = requests.get(url + method_url, params=params, headers=headers, verify=False)
        Response.LOGGER.info('Request url {}{} with params {}, headers {}'.format(url, method_url, params, headers))
        if response.status_code == 404:
            Response.LOGGER.info('Response {}'.format(response))
        else:
            Response.LOGGER.info('Response {}{}'.format(response, response.json()))
        return response


class PydanticResponseError:
    @staticmethod
    def print_error(e):
        print(BColors.WARNING + "\n__________<ReportValidate>__________" + BColors.ENDC)
        print(BColors.BOLD + "Ошибка валидации, тип:" + BColors.ENDC,
              BColors.FAIL + repr(e.errors()[0]['type']),
              ":", repr(e.errors()[0]['msg']) + BColors.ENDC)
        print(BColors.BOLD + "Проблемный ключ:" + BColors.ENDC, repr(e.errors()[0]['loc']))
        print(BColors.BOLD + "Входящее значение:" + BColors.ENDC, repr(e.errors()[0]['input']))
        print(BColors.BOLD + "Полный текст ошибки:" + BColors.ENDC, repr(e.errors()))
        print(BColors.WARNING + "__________</ReportValidate>__________" + BColors.ENDC)


