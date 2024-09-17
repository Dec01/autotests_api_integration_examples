import os
from dotenv import load_dotenv

load_dotenv()
class PathsServices:

    service_domains = {
        'Pim': os.getenv('PIM_DOMAIN'),
        'Service': os.getenv('SERVICE_DOMAIN'),
        'BFFService': os.getenv('BFF_DOMAIN'),
        'SHOP': os.getenv('SHOP_DOMAIN'),
        'Kafka': os.getenv('KAFKA_DOMAIN')
    }

    health_paths = {
        'Pim': '/',
        'Service': '/_health',
        'BFFService': '/_health',
        'SHOP': '/_health'
    }

    service_bff_paths = {
        'BFFCatalogService': {
            'CatalogProduct': '/v1/catalog/product',
            'CatalogCategory': '/v1/catalog/category'
        }
    }

    service_pim_paths = {
        'PimProduct': {
            'PublicProduct': '/tests/public_product',
            'UnpublicProduct': '/tests/unpublic_product',
            'LinkCategory': '/tests/link_category',
            'UnLinkCategory': '/tests/unlink_category'

        }
    }

    service_catalog_paths = {
        'ServiceProduct': {
            'ProductSlug': '/v1/catalog/product/'
        }
    }

    service_majento_paths = {
        'ShopServiceStage': {
            'Token': '/v1/token',
            'Stock': '/v1/getStock/',
            'Price': '/v1/getPrice/',
        }
    }
