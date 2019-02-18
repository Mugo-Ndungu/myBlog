import os


class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://alex:aaronmichelle@localhost/pichsss'
    SQLALCHEMY_TRACK_NOTIFICATIONS=False
    SECRET_KEY='Paula1234!'
    UPLOADED_PHOTOS_DEST='app/static/photos'
    # email configurations
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='twinnymugo@gmail.com'
    MAIL_PASSWORD='Paula1234!'
    SUBJECT_PREFIX='BLOG HUB'
    SENDER_EMAIL='twinnymugo@gmail.com'


class ProdConfig(Config):
    '''
    Production  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URI")

class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}