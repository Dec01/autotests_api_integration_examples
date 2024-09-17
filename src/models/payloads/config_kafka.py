import os
from dotenv import load_dotenv

load_dotenv()


class ConfigKafka:

    general_config = {
                'group.id': 'test-autotest',
                'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'SCRAM-SHA-512',
                'ssl.ca.location': 'src/YandexInternalRootCA.crt',
                'sasl.username': os.getenv('KAFKA_SASL_PLAIN_USERNAME'),
                'sasl.password': os.getenv('KAFKA_SASL_PLAIN_PASSWORD'),
                'auto.offset.reset': 'latest',
                'session.timeout.ms': 180000,
                'heartbeat.interval.ms': 181000
    }

    cleaning_config = {
                'group.id': 'test-autotest',
                'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
                'security.protocol': 'SASL_SSL',
                'sasl.mechanism': 'SCRAM-SHA-512',
                'ssl.ca.location': 'src/YandexInternalRootCA.crt',
                'sasl.username': os.getenv('KAFKA_SASL_PLAIN_USERNAME'),
                'sasl.password': os.getenv('KAFKA_SASL_PLAIN_PASSWORD'),
                'auto.offset.reset': 'latest',
                'session.timeout.ms': 10000,
                'heartbeat.interval.ms': 11000
    }
