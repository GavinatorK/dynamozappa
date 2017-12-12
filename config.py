
# config.py
import os

class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SECRET_KEY="my-precious"
    SECURITY_PASSWORD_SALT="my-precious-two"
    # SQLALCHEMY_ECHO = True
      # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    #MAIL_SERVER='gmail-smtp-in.l.google.com'
    MAIL_DEBUG=True
    MAIL_PORT = 465
    #MAIL_PORT=25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'brocas.king@gmail.com'

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
