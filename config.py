# myServer/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = basedir
EYECATCH = 'SERVER'
EXECUTION_MODE = 'development'
DEBUG = True
# Secret key for signing cookies
SECRET_KEY = 'p9Bv<3Eid9%$i01'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'aeiotheosomegasgeometreip9Bv<3Eid9%$i01'
SECURITY_PASSWORD_SALT = 'aeiotheosomegasgeometreip9Bvtispaolas'
################################################
# mail server
################################################
#define in ..instance as environment variable
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
################################################
# mail accounts
################################################
MAIL_SENDER = 'noreply@ganimides.com>'
MAIL_SUBJECT_PREFIX = '[ganimides]'
MAIL_DEFAULT_SENDER = 'noreply@ganimides.com'
MAIL_ADMIN_SENDER = 'admin@ganimides.com'
MAIL_SUPPORT_SENDER = 'support@ganimides.com'
WEBSITE_ADMIN = os.environ.get('WEBSITE_ADMIN')
#############################################################################################
#google recapcha
#############################################################################################
RECAPTCHA_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
RECAPTCHA_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
RECAPTCHA_INVISIBLE_SITE_KEY=os.environ["RECAPTCHA_INVISIBLE_SITE_KEY"]
RECAPTCHA_INVISIBLE_SECRET_KEY=os.environ["RECAPTCHA_INVISIBLE_SECRET_KEY"]
RECAPTCHA_PUBLIC_KEY=os.environ["RECAPTCHA_SITE_KEY"]
RECAPTCHA_PRIVATE_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
GOOGLE_RECAPTCHA_CHECKBOX_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
GOOGLE_RECAPTCHA_CHECKBOX_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY=os.environ["RECAPTCHA_SITE_KEY"]
GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY=os.environ["RECAPTCHA_SECRET_KEY"]
#+config params
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'light'}
# or RECAPTCHA_DATA_ATTRS = {'theme': 'dark','size':'compact'}
#RECAPTCHA_ENABLED = True
#RECAPTCHA_SITE_KEY = GOOGLE_RECAPTCHA_CHECKBOX_SITEKEY
#RECAPTCHA_SECRET_KEY = GOOGLE_RECAPTCHA_CHECKBOX_SECRETKEY
#RECAPTCHA_THEME = "light"
#RECAPTCHA_TYPE = "image"
#RECAPTCHA_SIZE = "normal"
#RECAPTCHA_RTABINDEX = 0
################################################
# limits
################################################
FLASKY_POSTS_PER_PAGE = 20
FLASKY_FOLLOWERS_PER_PAGE = 50
FLASKY_COMMENTS_PER_PAGE = 30
FLASKY_SLOW_DB_QUERY_TIME = 0.5
#############################################################################################
#server app folders (relative to the app folder)i.e.
#https://www.pythonanywhere.com/user/ganimides/files/home/ganimides/mysite/
#############################################################################################
#relative to mysite which is https://www.pythonanywhere.com/user/ganimides/files/home/ganimides/ganimides_website
PICTURES_FOLDER = '../static/pictures/'
IMAGES_FOLDER = '../../static/images/'
FLAGS_FOLDER = '../static/images/flags/'
ICONS_FOLDER = '../static/images/icons/'
UPLOAD_FOLDER = '../static/Uploads/'
TEMPLATES_ROOT_FOLDER = 'website_app/templates'
#relative to flask templates which is https://www.pythonanywhere.com/user/ganimides/files/home/ganimides/ganimides_website/website_app/templates
LAYOUTS_FOLDER = 'base_layouts/'
TEMPLATES_FOLDER = 'templates/'
PAGES_FOLDER = 'page_contents/'
FORMS_FOLDER = 'page_forms/'
COMPONENTS_FOLDER = 'page_components/'
#############################################################################################
#components folders: authorization etc
#############################################################################################
AUTHORIZATION_FOLDER = 'authorization/'
#############################################################################################
#for upload files pictures avatars etc
#############################################################################################
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #Ths code will limit the maximum allowed payload to 16 megabytes.  If a larger
                                      #file is transmitted, Flask will raise a RequestEntityTooLarge exception.
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])
#############################################################################################
#other
#############################################################################################
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
CSRF_SESSION_KEY = "aeiotheosomegasgeometrei"
#############################################################################################
#print('###config###',EYECATCH,'RECAPTCHA_SITE_KEY',RECAPTCHA_SITE_KEY,os.environ["RECAPTCHA_SITE_KEY"])