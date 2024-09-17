import json
import os

data_object_file = os.path.join('.', 'data_object.json')
data_object_price_file = os.path.join('.', 'data_object_price.json')

class DataTestedObject:

    @staticmethod
    def save_data_product(data):
        with open(data_object_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_data_product():
        with open(data_object_file, "rb") as f:
            return json.load(f)

    @staticmethod
    def save_price_product(data):
        with open(data_object_price_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_price_product():
        with open(data_object_price_file, "rb") as f:
            return json.load(f)

    @staticmethod
    def get_product_id():
        product_json = DataTestedObject.load_data_product()
        product_id = product_json['items'][0]['uuid']
        char = '_'
        idx = product_id.find(char)
        if idx != -1:
            product_id = product_id[:idx]
        else:
            product_id = ""
        return product_id

    @staticmethod
    def get_product_id_to_kafka():
        product_json = DataTestedObject.load_data_product()
        product_id = product_json['items'][0]['uuid']
        return product_id

    @staticmethod
    def get_product_id_price():
        product_json = DataTestedObject.load_data_product()
        product_id_price = product_json['items'][0]['price']
        return product_id_price

    @staticmethod
    def get_product_price():
        product_json = DataTestedObject.load_price_product()
        product_price = product_json[0]
        char = '.'
        idx = product_price.find(char)
        if idx != -1:
            product_price = product_price[:idx]
        else:
            product_price = ""
        return product_price

    @staticmethod
    def get_product_slug():
        product_json = DataTestedObject.load_data_product()
        product_slug = product_json['items'][0]['code']
        return product_slug

    @staticmethod
    def get_product_sku():
        product_json = DataTestedObject.load_data_product()
        product_slug = product_json['items'][0]['price']['sku']
        return product_slug
