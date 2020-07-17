from celery import Celery
import Config
import redis


#使用rabbitmq
# broker = 'amqp://{}:{}@{}:{}/'.format(Config.RABBITMQ_USER, Config.RABBITMQ_PWD, Config.RABBITMQ_HOSTS, Config.RABBITMQ_PORT)
# turkey_app = Celery('turkey_app',
#              broker=broker+Config.TURKEY_VHOST)

#以个人redis作为中间件
# broker = 'redis://' + Config.PERSONAL_REDIS_HOST + ':' + Config.REDIS_PROT + '/' + Config.TEST_BROKER_DB


broker = 'redis://' + Config.COMPANY_REDIS + ':' + Config.REDIS_PROT + '/' + Config.TEST_BROKER_DB

print(broker)

turkey_app = Celery('turkey_app',
             broker=broker)


if __name__ == '__main__':
    print(broker)