# module_authorization database init
"""
This script creates default database entries
"""
# # # #
import os
import sqlalchemy
#from sqlalchemy.engine.url import URL
#import pymysql
#pymysql.install_as_MySQLdb()
#import MySQLdb
#from sqlalchemy import create_engine
#from flask_sqlalchemy import SQLAlchemy
from .. import db
from .. import app as application
app = application
app.app_context().push()

from .models import Subscriber, ContactMessage

DATABASE_SERVER = app.config['DATABASE_SERVER']
DATABASE_SERVER_URI = app.config['DATABASE_SERVER_URI']
DATABASE_NAME = app.config['DATABASE_NAME']
DATABASE_URI = app.config['DATABASE_URI']

#print(__name__,'@@@@DATABASE_SERVER_URI@@@',DATABASE_SERVER_URI)
#print(__name__,'@@@@DATABASE_URI@@@',DATABASE_URI)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def create_database():
    #print('   ', 'database-init', __name__, 'create the database if not exists')
    #print('   ', 'database-init', __name__, '   DATABASE_SERVER_URI =',DATABASE_SERVER_URI)
    dbserver_engine = sqlalchemy.create_engine(DATABASE_SERVER_URI, pool_recycle=280) # connect to server
    existing_databases = dbserver_engine.execute("SHOW DATABASES;")
    existing_databases = [d[0] for d in existing_databases]
    # for database in existing_databases:
    #     print("...database {0} on dbserver {1}".format(database, DATABASE_SERVER_URI))
    if DATABASE_NAME not in existing_databases:
        dbserver_engine.execute("CREATE DATABASE {db}".format(db=DATABASE_NAME))
        print('   ', 'database-init', __name__,"   {0} database CREATED on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
    else:
        print('   ', 'database-init', __name__, "   database {0} already exists on DBserver {1}".format(DATABASE_NAME, DATABASE_SERVER))
    # -or-
    # dbserver_engine.execute("CREATE DATABASE IF NOT EXISTS {db}".format(db=DATABASE_NAME))
    # dbserver_engine.execute("USE {db}".format(db=DATABASE_NAME))
    dbserver_engine.dispose()

def create_all_tables_auto():
    #print('   ', 'database-init', __name__, 'create all tables in database if not exists(auto)')
    #print('   ', 'database-init', __name__, '   DATABASE_URI =',DATABASE_URI)
    db_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=280) # connect to database
    existing_tables_before = db_engine.execute('SHOW TABLES;')
    existing_tables_before = [d[0] for d in existing_tables_before]
    #print('   ', 'database-init', __name__, 'tables before')
    #list_tables(db_engine)
    db.create_all(app=app)
    db.session.commit()
    existing_tables_after = db_engine.execute('SHOW TABLES;')
    existing_tables_after = [d[0] for d in existing_tables_after]
    created = 0
    for table in existing_tables_after:
        if table not in existing_tables_before:
            created = created + 1
    print('   ', 'database-init', __name__,"   {0} tables created in database {1}".format(created,DATABASE_NAME))
    db_engine.dispose()

def create_all_tables_manually():
    #print('   ', 'database-init', __name__, 'create tables in database if not exists (manually)')
    #print('   ', 'database-init', __name__, '   DATABASE_URI =', DATABASE_URI)
    db_engine = sqlalchemy.create_engine(DATABASE_URI, pool_recycle=280) # connect to database
    existing_tables = db_engine.execute('SHOW TABLES;')
    existing_tables = [d[0].lower() for d in existing_tables]

    thistable=Subscriber.__table__.name
    if thistable.lower() not in existing_tables:
        Subscriber.__table__.create(db_engine)
        print('   ', 'database-init', __name__,"   table {0} created in database {1}".format(thistable,DATABASE_NAME))

    thistable=ContactMessage.__table__.name
    if thistable.lower() not in existing_tables:
        ContactMessage.__table__.create(db_engine)
        print('   ', 'database-init', __name__,"   table {0} created in database {1}".format(thistable,DATABASE_NAME))

    existing_tables_after = db_engine.execute('SHOW TABLES;')
    existing_tables_after = [d[0] for d in existing_tables_after]
    created = 0
    for table in existing_tables_after:
        if table not in existing_tables:
            created = created + 1

    db_engine.dispose()
    print('   ', 'database-init', __name__,"   {0} tables created in database {1}".format(created,DATABASE_NAME))


def create_subscribers():
    #print('   ', 'database-init', __name__, 'create default Subscribers')
    created = 0
    users = [
        ('fredericos@leandrou.com', 'Fredericos', 'Leandrou', 'admin')
        ,('philippos@leandrou.com', 'Philippos', 'Leandrou', 'admin')
        ,('spithas@leandrou.com', 'Spithas', 'Leandrou', 'admin')
        ,('admin@leandrou.com', 'admin', 'admin', 'admin')
        ]
    for user in users:
        email = user[0]
        if not Subscriber.query.filter_by(email=email).first():
            thisUser = Subscriber(email=user[0], firstName=user[1], lastName=user[2])
            #db.session.add(thisUser)
            created = created + 1
            print('   ', 'database-init', __name__, '   subscriber created:', thisUser)
    #db.session.commit()
    print('   ', 'database-init', __name__,"   {0} Subscribers created in database {1}".format(created, DATABASE_NAME))

def list_tables(db_engine):
    print('   ', 'database-init', __name__, 'tables in database:',DATABASE_URI)
    #db_engine = sqlalchemy.create_engine(DATABASE_URI) # connect to database
    existing_tables = db_engine.execute('SHOW TABLES;')
    existing_tables = [d[0] for d in existing_tables]
    t = 0
    for table in existing_tables:
        t = t +1
        print('   ', 'database-init', __name__,"   {0}. {1}.{2}".format(t, DATABASE_NAME,table))
    #db_engine.dispose()

def tables_list(db_engine):
    #db_engine = sqlalchemy.create_engine(DATABASE_URI) # connect to database
    tables_list = db_engine.execute('SHOW TABLES;')
    tables_list = [d[0] for d in tables_list]
    #db_engine.dispose()
    return tables_list

def init_database():
    print('')
    print('   ', 'database-init', __name__, '######################################################')
    create_database()
    create_all_tables_auto()
    #create_all_tables_manually()
    #create_subscribers()
    print('   ', 'database-init', __name__, '######################################################')
    print('')

if __name__ == '__main__':
    cls()# now, to clear the screen
    init_database()
