class BaseConfig(object):
    DB_HOST='localhost'
    DB_PORT=27017


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    RESOURCES_PATH='resources'
    DB_NAME='paranuara'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    RESOURCES_PATH='test_resources'
    DB_NAME='test'


