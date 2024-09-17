import json
import pytest
import time
import requests

from confluent_kafka import Consumer, KafkaException
from pydantic import ValidationError

from src.models.paths.paths_services import PathsServices
from src.models.payloads.model_health import ResponsesCheck
from src.models.payloads.model_bff_catalog_product import PayloadBffCatalogProduct
from src.models.payloads.model_pim import PayloadPim
from src.models.processings.request_headers import RequestAuth
from src.models.payloads.model_testing_object import DataTestedObject
from src.models.payloads.config_kafka import ConfigKafka

health_test = PathsServices.health_paths.items()
timing = time.time()

class TestPublicationProduct:

    @pytest.mark.parametrize('health_test', health_test, ids=['Pim', 'CatalogService', 'BFFSevice', 'Shop'])
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

    def test_case_1__bff_analysis_and_save_product_date(self, domain, req):
        domain_path = domain.service_domain_definition("BFFService")
        method_path = PathsServices.service_bff_paths.get('BFFCatalogService').get('CatalogProduct')
        payload = PayloadBffCatalogProduct.request_generation()
        try:
            response = req.post_request(domain_path, method_path, {}, payload, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert PayloadBffCatalogProduct.response_validate(data)
            DataTestedObject.save_data_product(data)
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

    def test_case_2__majento_analysis_and_save_product_price(self, domain, req):
        headers = RequestAuth.majento
        domain_path = domain.service_domain_definition("Shop")
        method_path = PathsServices.service_majento_paths.get('ShopServiceStage').get('Price')
        product_sku = DataTestedObject.get_product_sku()
        product_price = DataTestedObject.get_product_id_price()
        try:
            response = req.get_request(domain_path, method_path + product_sku, {}, headers)
            data = response.json()
            if product_price == 0:
                assert response.status_code == 200 or response.status_code == 404, 'check StatusCode: 404'
            else:
                assert response.status_code == 200, 'check StatusCode: 200'
                DataTestedObject.save_price_product(data)
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

    def test_case_3__pim_unpublic_product(self, domain, req):
        domain_path = domain.service_domain_definition("Pim")
        method_path = PathsServices.service_pim_paths.get('PimProduct').get('UnpublicProduct')
        headers = RequestAuth.pim
        product_id = DataTestedObject.get_product_id()
        payload = PayloadPim.request_generation(product_id)
        try:
            response = req.post_request(domain_path, method_path, {}, payload, headers)
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert PayloadPim.response_validate(data)
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

    def test_case_3_1_kafka_unpublic_product(self):
        product_id = DataTestedObject.get_product_id_to_kafka()
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
                    assert data['id'] == product_id
                    assert data['event'] == 'delete'
                    break
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def test_case_4__catalog_check_unpublic_product(self, domain, req):
        time.sleep(5)
        domain_path = domain.service_domain_definition("CatalogService")
        method_path = PathsServices.service_catalog_paths.get('CatalogServiceProduct').get('ProductSlug')
        product_slug = DataTestedObject.get_product_slug()
        try:
            response = req.get_request(domain_path, method_path + product_slug, {}, {})
            assert response.status_code == 404, 'check StatusCode: 200'
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

    def test_case_5__pim_public_product(self, domain, req):
        domain_path = domain.service_domain_definition("Pim")
        method_path = PathsServices.service_pim_paths.get('PimProduct').get('PublicProduct')
        headers = RequestAuth.pim
        product_id = DataTestedObject.get_product_id()
        payload = PayloadPim.request_generation(product_id)
        try:
            response = req.post_request(domain_path, method_path, {}, payload, headers)
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert PayloadPim.response_validate(data)
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

    def test_case_5_1_kafka_public_product(self):
        product_id = DataTestedObject.get_product_id_to_kafka()
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
                    assert data['id'] == product_id
                    assert data['event'] == 'create'
                    break
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def test_case_6__catalog_check_public_and_price_product(self, domain, req):
        time.sleep(10)
        domain_path = domain.service_domain_definition("CatalogService")
        method_path = PathsServices.service_catalog_paths.get('CatalogServiceProduct').get('ProductSlug')
        product_slug = DataTestedObject.get_product_slug()
        product_price = DataTestedObject.get_product_price()
        try:
            response = req.get_request(domain_path, method_path + product_slug, {}, {})
            data = response.json()
            assert response.status_code == 200, 'check StatusCode: 200'
            assert data['price']['priceStructure']['basePrice'] == int(product_price), 'Check price'
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



