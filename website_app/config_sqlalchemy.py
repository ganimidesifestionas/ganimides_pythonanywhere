"""SQLALCHEMY configurations sqlalchemy_config.py"""
import os
from website_app.debug_services.debug_log_services import *


log_module_start('sqlalchemy_configuration')

EYECATCH = 'SQLALCHEMY'


# sqlalchemy
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 60 #less than SQLALCHEMY_POOL_RECYCLE
SQLALCHEMY_POOL_RECYCLE = 100 #greater than SQLALCHEMY_POOL_TIMEOUT
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_MAX_OVERFLOW = 5
if os.environ.get("SQLALCHEMY_DATABASE_URI"):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
if not SQLALCHEMY_DATABASE_URI:
    DATABASE_URL = os.environ.get('DATABASE_URI')
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
################################################################
log_variable('SQLALCHEMY_ECHO', SQLALCHEMY_ECHO)
log_variable('SQLALCHEMY_RECORD_QUERIES', SQLALCHEMY_RECORD_QUERIES)
log_variable('SQLALCHEMY_TRACK_MODIFICATIONS', SQLALCHEMY_TRACK_MODIFICATIONS)
log_variable('SQLALCHEMY_POOL_SIZE', SQLALCHEMY_POOL_SIZE)
log_variable('SQLALCHEMY_POOL_RECYCLE', SQLALCHEMY_POOL_RECYCLE)
log_variable('SQLALCHEMY_POOL_TIMEOUT', SQLALCHEMY_POOL_TIMEOUT)
log_variable('SQLALCHEMY_MAX_OVERFLOW', SQLALCHEMY_MAX_OVERFLOW)
log_variable('SQLALCHEMY_COMMIT_ON_TEARDOWN', SQLALCHEMY_COMMIT_ON_TEARDOWN)
log_variable('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)
################################################################

log_module_finish('sqlalchemy_configuration')



################################################
# SQLALCHEMY
################################################
#SQLALCHEMY_POOL_RECYCLE = 90
#SQLALCHEMY_POOL_TIMEOUT = 90
#SQLALCHEMY_POOL_SIZE = 5
#SQLALCHEMY_POOL_RECYCLE = -1
#SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# mysql> show global variables like "wait_timeout";
# +---------------+-------+
# | Variable_name | Value |
# +---------------+-------+
# | wait_timeout  | 300   |
# +---------------+-------+
# 1 row in set (0.00 sec)
# mysql> show global variables like "%timeout%";
# +-----------------------------+----------+
# | Variable_name               | Value    |
# +-----------------------------+----------+
# | connect_timeout             | 10       |
# | delayed_insert_timeout      | 300      |
# | have_statement_timeout      | YES      |
# | innodb_flush_log_at_timeout | 1        |
# | innodb_lock_wait_timeout    | 50       |
# | innodb_rollback_on_timeout  | OFF      |
# | interactive_timeout         | 28800    |
# | lock_wait_timeout           | 31536000 |
# | net_read_timeout            | 30       |
# | net_write_timeout           | 60       |
# | rpl_stop_slave_timeout      | 31536000 |
# | slave_net_timeout           | 60       |
# | wait_timeout                | 300      |
# +-----------------------------+----------+
# 13 rows in set (0.01 sec)
#SQLALCHEMY_POOL_SIZE = 5
#SQLALCHEMY_POOL_TIMEOUT = 60
# SQLALCHEMY_POOL_RECYCLE = 10
# SQLALCHEMY_POOL_SIZE = 5
# SQLALCHEMY_POOL_TIMEOUT = 60 #less than SQLALCHEMY_POOL_RECYCLE
# SQLALCHEMY_POOL_RECYCLE = 100 #greater than SQLALCHEMY_POOL_TIMEOUT
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#SQLALCHEMY_MAX_OVERFLOW = 5
################################################
# '''
# pool_recycle=-1: this setting causes the pool to recycle
#     connections after the given number of seconds has passed. It
#     defaults to -1, or no timeout. For example, setting to 3600
#     means connections will be recycled after one hour. Note that
#     MySQL in particular will disconnect automatically if no
#     activity is detected on a connection for eight hours (although
#     this is configurable with the MySQLDB connection itself and the
#     server configuration as well).
# '''
# #    "charset": "utf8"
# #}
# import pymysql
# connection = pymysql.connect(host='***',
#                                  user='***',
#                                  password='***',
#                                  db='***',
#                                  charset='utf8mb4',
#                                  cursorclass=pymysql.cursors.DictCursor
#                                  )


# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimides_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db'
# #print('      ', SERVER_CONFIG_FOLDER, SERVER_CONFIG_FILE, '###instance### ###config.py### SQLALCHEMY_DATABASE_URI=',SQLALCHEMY_DATABASE_URI)
# username = "ganimides"
# password = "philea13"
# hostname = "ganimides.mysql.pythonanywhere-services.com"
# databasename = "ganimides$ganimides_db"
# database_username = "ganimides"
# database_password = "spithas13"
# SQLALCHEMY_DATABASE_URI2 = "mysql+{mysqlconnector}://{username}:{password}@{hostname}/{databasename}".format(
#     mysqlconnector="pymysql",
#     username="ganimides",
#     password="philea13",
#     hostname="ganimides.mysql.pythonanywhere-services.com",
#     databasename="ganimides$ganimides_db"
# )
# #db = SQLAlchemy(app, engine = create_engine("mysql+myqldb://ganimides:philea13@ganimides.mysql.pythonanywhere-services.com/ganimides$ganimides_db", pool_recycle=280))
# #mysql://InsulT:password@mysql.server/InsulT$default'
# #{
# #    "host": "localhost",
# #    "user": "root",
# #    "password": "philea13",
# #    "database": "db",
# #    "sql_engine": "mysql+pymysql",
# #    "charset": "utf8"
# #}
# #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# #DATABASE_CONNECT_OPTIONS = {}
