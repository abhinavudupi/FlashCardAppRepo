import os

baseDir = os.path.abspath(os.path.dirname(__file__))
class Config():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_TIMEZONE = "Asia/Kolkata"
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379

class LocalDevConfig(Config):
    user = 'abhinav'
    password = 'abhinavsql'
    host = 'localhost'
    port = 5432
    database = 'devdb'
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))
    DEBUG = True

class ProductionConfig(Config):
    user = 'flashcardApp'
    password = 'flashtest@123'
    host = 'localhost'
    port = 5432
    database = 'flashCardDB'
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, database))