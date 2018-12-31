import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key'
    MAIL_SERVER = os.environ.get('MAIL_SEVER', 'smtp.gmail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SNS_MAIL_SUBJECT_PREFIX = '[SNS]'
    SNS_MAIL_SENDER = 'SNS Admin <example@gmail.com>'
    SNS_ADMIN = os.environ.get('SNS_ADMIN')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SNS_POSTS_PER_PAGE = 20
    SNS_FOLLOWERS_PER_PAGE = 50
    SNS_COMMENTS_PER_PAGE = 30
    SNS_SLOW_DB_QUERY_TIME = 0.5


    @staticmethod
    def init_app(app):
        pass

    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        #email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.SNS_MAIL_SENDER,
            toaddrs=[cls.SNS_ADMIN],
            subject=cls.SNS_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


# class HerokuConfig(ProductionConfig):
#     SSL_REDIRECT = True if os.environ.get('DYNO') else False

#     @classmethod
#     def init_app(cls, app):
#         print("here!!")
#         ProductionConfig.init_app(app)

#         # handle reverse proxy server headers
#         from werkzeug.contrib.fixers import ProxyFix
#         app.wsgi_app = ProxyFix(app.wsgi_app)

#         # log to stderr
#         import logging
#         from logging import StreamHandler
#         file_handler = StreamHandler()
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)
        

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 'heroku': HerokuConfig,

    'default': DevelopmentConfig
}


