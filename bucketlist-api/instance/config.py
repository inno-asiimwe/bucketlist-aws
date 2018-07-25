"""Module contains configurations for the app"""
import os


class Config:
    """The Parent configurations for the app"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    TOKEN_TIME = 31536000


class DevelopmentConfig(Config):
    """Class for development configurations"""
    DEBUG = True


class TestingConfig(Config):
    """Class for the testing configurations"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@database:5432/test_db'
    TOKEN_TIME = 2


class StagingConfig(Config):
    """Class for the staging configurations"""
    DEBUG = True


class ProductionConfig(Config):
    """Class for the Production configurations"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s/%s' % (
        os.getenv('DBUSER'), os.getenv('DBPASS'), os.getenv('DBHOST'),
        os.getenv('DBNAME')
    )
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
