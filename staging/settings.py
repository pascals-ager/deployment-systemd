class BaseConfig(object):
    """Base configuration."""
    PROJECT = "vimcar"
    SECRET_KEY = 'thisissecret'
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@127.0.0.1:5432/vimcar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisisdevsecret'
    SALT_KEY = 'saltthisthing'

class TestConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@postgres/vimcartest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisistestsecret'
    SALT_KEY = 'saltthisthing'

class StageConfig(BaseConfig):
    """Staging configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@postgres/vimcartest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisistagingsecret'
    SALT_KEY = 'saltthisthing'

class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:vimcar@postgres/vimcartest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'thisisproductionsecret'
    SALT_KEY = 'saltthisthing'