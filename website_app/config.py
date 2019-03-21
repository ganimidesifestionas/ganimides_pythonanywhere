# application level config.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))
filename = os.path.basename(__file__)
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '')
print ('xxxxxxxxxxx',RECAPTCHA_PUBLIC_KEY)

class Config(object):
    """Common configurations"""
    # Put any configurations here that are common across all environments
    #
    # UPPER CASE
    #    
    EYECATCH = 'MYAPP'
    DEBUG = True

    # Secret key for signing cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'appconfig-aeiotheosomegasgeometreip9Bv<3Eid9%$i01'
    SECURITY_PASSWORD_SALT = 'appconfig-aeiotheosomegasgeometreip9Bvtispaolas'
    # company, application ids
    COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Leandrou Technology Forward')
    APPLICATION_NAME = os.environ.get('APPLICATION_NAME', 'WEBSITE')

    # session cookies expired in 5 minutes
    #PERMANENT_SESSION_LIFETIME =  timedelta(minutes=5)

    # mail accounts
    MAIL_SENDER = 'noreply@ganimides.com>'
    MAIL_SUBJECT_PREFIX = '[ganimides]'
    MAIL_DEFAULT_SENDER = 'noreply@ganimides.com'
    MAIL_ADMIN_SENDER = 'admin@ganimides.com'
    MAIL_SUPPORT_SENDER = 'support@ganimides.com'
    WEBSITE_ADMIN = os.environ.get('WEBSITE_ADMIN')

    # limits
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # application specific
    BASE_DIR = basedir
    COPYWRITE_YEAR = "2018"
    COMPANY_NAME = "Leandrou Technology Forward"
    COMPANY_COLOR = "blue"
    DOMAIN_NAME = "ganimedes.com"
    DOMAIN_TITLE = "Ganimides Business Technology Institute"
    DOMAIN_COLOR = "lightseagreen"
    CONTACT_EMAIL = "webmaster@ganimedes.com"
    COMPANY_ADDRESS = "4, vasilis michelides str.<br/>2015 dhasoupolis<br/>Nicosia<br/>Cyprus<br/>"
    COMPANY_PHONES = "00357.22311634"
    COMPANY_CONTACT_EMAIL = "contact@L&LTech.com"
    COMPANY_SUPPORT_EMAIL = "support@LeandrouTech.com"
    CONTACT_EMAIL = "contact@ganimedes.com"
    SUPPORT_EMAIL = "support@ganimedes.com"
    INQUIRY_EMAIL = "inquiry@ganimedes.com"
    WEBSITE_ADMIN_EMAIL = "admin@ganimedes.com"
    DEFAULT_LANGUAGE = 'cy'
    LANGUAGES = {
        'en': ['English','uk.png']
        ,'gr': ['Ελληνικά','greece.png']
        ,'cy': ['Κυπριακά','cyprus.png']
    }
    FLAGS = {
        'en': 'uk.png'
        ,'gr': 'greece.png'
        ,'cy': 'cyprus.png'
    }
    DEBUG_TYPES = {}
    DEBUG_VERSION = ''

    SPLASHFORM_LOGIN = 'splashform_login.html'
    SPLASHFORM_REGISTRATION = 'splashform_registration.html'
    SPLASHFORM_FORGETPASSWORD = 'splashform_forgetpassword.html'
    SPLASHFORM_CONTACTUS = 'splashform_contactus.html'

    #web server app folders
    #relative to mysite which is https://www.pythonanywhere.com/user/ganimides/files/home/ganimides/ganimides_website
    PICTURES_FOLDER = '/static/pictures/'
    IMAGES_FOLDER = '/static/images/'
    VIDEOS_FOLDER = '/static/videos/'
    FLAGS_FOLDER = '/static/images/flags/'
    ICONS_FOLDER = '/static/images/icons/'
    UPLOAD_FOLDER = '/static/Uploads/'
    TEMPLATES_ROOT_FOLDER = 'website_app/templates'
    #relative to flask templates which is https://www.pythonanywhere.com/user/ganimides/files/home/ganimides/ganimides_website/website_app/templates
    LAYOUTS_FOLDER = 'layout_components/'
    TEMPLATES_FOLDER = 'templates/'
    PAGES_FOLDER = 'page_contents/'
    FORMS_FOLDER = 'page_forms/'
    COMPONENTS_FOLDER = 'page_components/'
    EMAILS_FOLDER = 'email_templates/'
    SMS_FOLDER = 'sms_templates/'
    IMAGE_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])
    PICTURE_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])
    VIDEO_EXTENSIONS = set(['mp4', 'mp5'])

    #components folders: authorization etc
    AUTHORIZATION_FOLDER = 'authorization/'
    ADMINISTRATION_FOLDER = 'administration/'
    #for upload files pictures avatars etc
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024; #Ths code will limit the maximum allowed payload to 16 megabytes. If a larger file is transmitted, Flask will raise a RequestEntityTooLarge exception.
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])

    # mail server
    # MAIL_SERVER_PROVIDER = os.environ.get('MAIL_SERVER_PROVIDER', 'GOOGLE')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    #recapcha
    RECAPTCHA_IS_GOOGLE = True
    #RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '')
    #print ('xxxxxxxxxxx',RECAPTCHA_PUBLIC_KEY)
    #RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '')
    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'light'}
    # or RECAPTCHA_DATA_ATTRS = {'theme': 'dark','size':'compact'}
    RECAPTCHA_ENABLED = True
    #RECAPTCHA_THEME = "light"
    #RECAPTCHA_TYPE = "image"
    #RECAPTCHA_SIZE = "normal"
    #RECAPTCHA_RTABINDEX = 0

    # SQLALCHEMY
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    #SQLALCHEMY_POOL_SIZE = 5
    #SQLALCHEMY_POOL_TIMEOUT = 360
    #SQLALCHEMY_MAX_OVERFLOW = 

    # other config
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SSL_REDIRECT = False
    # Application threads:A common general assumption is using 2 per available processor cores - to handle incoming requests using one and performing background operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = "aeiotheosomegasgeometreibobbistarr"

#    @staticmethod
#    def init_app(app):
#        pass
############################################################
class DesignConfig(Config):
    """Design mode configurations"""
    EYECATCH = 'MYAPP-DESIGN'
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TYPES = {
        'LAYOUT'
        , 'TEMPLATE'
        , '*'
        }
    DEBUG_VERSION = '34'

class DevelopmentConfig(Config):
    """Development mode configurations"""
    EYECATCH = 'MYAPP-DEVELOPMENT'
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TYPES = {
        'LAYOUT'
        , 'TEMPLATE'
        , '*'
        }
    DEBUG_VERSION = '33'

class TestingConfig(Config):
    """Testing mode configurations"""
    EYECATCH = 'MYAPP-TESTING'
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TYPES = {
        '*'
        }
    DEBUG_VERSION = '32'

class SandBoxConfig(Config):
    """Sandbox mode configurations"""
    EYECATCH = 'MYAPP-SANDBOX'
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TYPES = {}
    DEBUG_VERSION = ''

class ProductionConfig(Config):
    """Production mode configurations """
    EYECATCH = 'MYAPP-PRODUCTION'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TYPES = {}
    DEBUG_VERSION = ''

class FlaskConfig(Config):
    """Flask configurations"""
    EYECATCH = 'APP-FLASK'
    DEBUG = False
    TESTING = True
    RECAPTCHA_IS_GOOGLE = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TYPES = {
        '*'
        }
    DEBUG_VERSION = ''

class xProductionConfig(Config):
    EYECATCH = 'MYAPP-PRODUCTION'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
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
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

###################################################################################
class LocalHostConfig(Config):
    EYECATCH = 'MYAPP-ON-LOCALHOST'

class PythonAnyWhereConfig(Config):
    EYECATCH = 'MYAPP-ON-PYTHONANYWHERE'

class HerokuConfig(Config):
    EYECATCH = 'MYAPP-ON-HEROKU'
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)

#config = {
#    'development': DevelopmentConfig,
#    'testing': TestingConfig,
#    'production': ProductionConfig,
#    'heroku': HerokuConfig,
#    'docker': DockerConfig,
#    'unix': UnixConfig,
#    'default': DevelopmentConfig
#}

#####################################################
execmode_config = {
    'design' : DesignConfig
    ,'development' : DevelopmentConfig
    ,'testing' : TestingConfig
    ,'sandbox' : SandBoxConfig
    ,'production' : ProductionConfig
}
#####################################################
environment_config = {
    'localhost' : LocalHostConfig
    ,'heroku' : HerokuConfig
    ,'pythonanywhere' : PythonAnyWhereConfig
    ,'heroku' : HerokuConfig
    ,'pythonanywhere' : PythonAnyWhereConfig
}
#####################################################
app_config = {
    'flask' : FlaskConfig
}
#####################################################
