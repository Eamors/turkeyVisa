class Config(object):
	pass


class ProdConfig(Config):
	pass


class DevConfig(Config):
	# DEBUG = True
	DEBUG = False


REDIS_HOST = '127.0.0.1'
PERSONAL_REDIS_HOST = '49.233.181.211'
COMPANY_REDIS = '8.210.183.162'
REDIS_PROT = '6379'
BROKER_DB = '1'
BACKEND_DB = '2'
CACHE_DB = '3'
HOT_BROKER_DB = '4'
TEST_BROKER_DB = "5"

RABBITMQ_HOSTS = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'admin'
RABBITMQ_PWD = 'qq123456'




TURKEY_VHOST = 'turkey_spider'
