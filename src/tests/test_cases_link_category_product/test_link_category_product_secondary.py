import json
import pytest
import time
import requests

from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException
from pydantic import ValidationError
from src.models.paths.paths_services import PathsServices
from src.models.payloads.model_health import ResponsesCheck
from src.models.payloads.model_pim_links_category_product import PayloadPimPostLinkCategoryProduct
from src.models.payloads.model_post_bff_catalog_product import PayloadBffPostCatalogProduct
from src.models.processings.request_headers import RequestAuth
from src.models.payloads.config_kafka import ConfigKafka

load_dotenv()
health_test = PathsServices.health_paths.items()
timing = time.time()

class TestLinkCategoryProductMain:

    @pytest.mark.parametrize('health_test', health_test, ids=['Pim', 'Service', 'BFFSevice', 'Shop'])
    def test_case_0__health_check_services(self, domain, req, health_test):
        domain_path = domain.service_domain_definition(health_test[0])
        method_path = health_test[1]
        try:
            if health_test[0] == 'Shop':
                payload = ResponsesCheck.request_health_check_shop()
                response = req.post_request(domain_path, method_path, {}, {'query': payload}, {})
                data = response.json()
                assert response.status_code == 200, 'check StatusCode: 200'
                assert ResponsesCheck.response_health_check(health_test[0], data)
            else:
                response = req.get_request(domain_path, method_path, {}, {})
                data = response.json()
                assert response.status_code == 200, 'check StatusCode: 200'
                assert ResponsesCheck.response_health_check(health_test[0], data)
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False

    def test_case_0_1_clear_kafka_message_and_health_check_topic(self):
        consumer = Consumer(ConfigKafka.cleaning_config)
        consumer.subscribe(['product-catalog'])

        try:
            while True:
                msg = consumer.poll(0)
                if msg is None:
                    if time.time() - timing > 5.0:
                        break
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value().decode('utf-8'))
                    if data:
                        print("msg: PASS")
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def test_case_1__bff_check_old_link_category_product_main (self, domain, req):
        domain_path = domain.service_domain_definition("BFFService")
        method_path = PathsServices.service_bff_paths.get('BFFCatalogService').get('CatalogProduct')
        try:
            response = req.get_request(domain_path, method_path + '/fizika-7-klass', {}, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert data['payload']['category']['id'] == '123456'
            assert data['payload']['category']['parentId'] == '123456'
            assert data['payload']['category']['code'] == 'tetradi'
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False


    def test_case_2__pim_link_new_second_category(self, domain, req):
        time.sleep(3)
        domain_path = domain.service_domain_definition("Pim")
        method_path = PathsServices.service_pim_paths.get('PimProduct').get('LinkCategory')
        headers = RequestAuth.pim
        payload = PayloadPimPostLinkCategoryProduct.request_generation(12345, 12345, False)
        try:
            response = req.post_request(domain_path, method_path, {}, payload, headers)
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert PayloadPimPostLinkCategoryProduct.response_validate(data)
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False

    def test_case_2_1_kafka_link_second_category(self):
        consumer = Consumer(ConfigKafka.general_config)
        consumer.subscribe(['product-catalog'])

        try:
            while True:
                msg = consumer.poll(0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value().decode('utf-8'))
                    assert data['event'] == 'update'
                    assert data['name']['ru'] == 'Физика. 7 класс.'
                    assert data['LinkCategories'][0]['marketCategories'][0] == '123344'
                    assert data['LinkCategories'][0]['marketCategories'][1] == '123454'
                    assert data['LinkCategories'][0]['mainCategory'] == '12342314'

                    break
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def test_case_3__bff_check_main_link_category_product(self, domain, req):
        time.sleep(5)
        domain_path = domain.service_domain_definition("BFFService")
        method_path = PathsServices.service_bff_paths.get('BFFCatalogService').get('CatalogProduct')
        try:
            response = req.get_request(domain_path, method_path + '/fizika-7-klass', {}, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert data['category']['id'] == '123456'
            assert data['category']['parentId'] == '123456'
            assert data['category']['code'] == 'tetradi'
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False

    def test_case_4__bff_check_second_link_category_product(self, domain, req):
        time.sleep(5)
        payload = PayloadBffPostCatalogProduct.request_generation('uchebniki', 'Физика. 7 класс.')
        domain_path = domain.service_domain_definition("BFFService")
        method_path = PathsServices.service_bff_paths.get('BFFCatalogService').get('CatalogProduct')
        try:
            response = req.post_request(domain_path, method_path, {}, payload, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert data['items'][0]['name'] == 'Физика. 7 класс.'
            assert data['items'][0]['id'] == '02_printedBook'
            assert data['items'][0]['code'] == 'fizika-7-klass'
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False


    def test_case_5__pim_unlink_second_category(self, domain, req):
        domain_path = domain.service_domain_definition("Pim")
        method_path = PathsServices.service_pim_paths.get('PimProduct').get('UnLinkCategory')
        headers = RequestAuth.pim
        payload = PayloadPimPostLinkCategoryProduct.request_generation(123456, 123456, False)
        try:
            response = req.post_request(domain_path, method_path, {}, payload, headers)
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert PayloadPimPostLinkCategoryProduct.response_validate(data)
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False

    def test_case_5_1_kafka_unlink_second_category(self):
        consumer = Consumer(ConfigKafka.general_config)
        consumer.subscribe(['product-catalog'])

        try:
            while True:
                msg = consumer.poll(0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    data = json.loads(msg.value().decode('utf-8'))
                    assert data['event'] == 'update'
                    assert data['name']['ru'] == 'Физика. 7 класс.'
                    assert data['LinkCategories'][0]['marketCategories'][0] == '123456'
                    assert data['LinkCategories'][0]['mainCategory'] == '123456'

                    break
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def test_case_6__bff_check_main_link_category_product_main (self, domain, req):
        time.sleep(5)
        domain_path = domain.service_domain_definition("BFFService")
        method_path = PathsServices.service_bff_paths.get('BFFCatalogService').get('CatalogProduct')
        try:
            response = req.get_request(domain_path, method_path + '/fizika-7-klass', {}, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert data['category']['id'] == '1234567'
            assert data['category']['parentId'] == '123456'
            assert data['category']['code'] == 'tetradi'
        except ValidationError as exc:
            print(repr(exc.errors()[0]['type']))
            assert False
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            assert False
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            assert False
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            assert False
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            assert False
