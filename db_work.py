#1:define database URL
import sqlalchemy
from sqlalchemy.engine.url import URL
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

from sqlalchemy import create_engine

mysql_engine = create_engine('mysql://{0}:{1}@{2}:{3}'.format('root', 'philea13', 'PHILIPPOS', 3306))


#db = MySQLdb.connect("localhost" , "root" , "password")
# conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')
# cur = conn.cursor()
# cur.execute("SELECT Host,User FROM user")
# for r in cur:
#     print(r)
# cur.close()
# conn.close()

postgres_db = {'drivername': 'postgres',
               'username': 'postgres',
               'password': 'postgres',
               'host': '192.168.99.100',
               'port': 5432}
sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}
mysql_db = {'drivername': 'mysql',
               'username': 'ganimedes',
               'password': 'philea13',
               'host': 'localhost',
               'port': 3306}
#print(URL(**postgres_db))
#print(URL(**sqlite_db))
print(URL(**mysql_db))
print('------------------------------')

# username = "ganimides"
# password = "philea13"
# hostname = "PHILIPPOS" #"ganimides.mysql.pythonanywhere-services.com"
# databasename = "ganimides_db"
# #databasename = "ganimides$ganimides_db"
# #database_username = "ganimides"
# #database_password = "spithas13"
# mysql_db_uri = "{drivername}+{mysqlconnector}://{username}:{password}@{hostname}/{databasename}".format(
#     drivername="mysql",
#     mysqlconnector="pymysql",
#     username="ganimides",
#     password="philea13",
#     hostname="PHILIPPOS", #"localhost", "ganimides.mysql.pythonanywhere-services.com",
#     databasename="ganimides_db"
# )

print('')
database_username="root"
database_password="philea13"
#################################
#2: create database server engine
#################################
DBserverURI = "{drivername}+{mysqlconnector}://{username}:{password}@{hostname}".format(
    drivername="mysql"
    ,mysqlconnector="pymysql"
    ,username="ganimedes"
    ,password="philea13"
    ,hostname="localhost" #, "ganimides.mysql.pythonanywhere-services.com",
    ,databasename="ganimedes_db"
)
print('DBserverURI =',DBserverURI)
print('------------------')

#dbserver_engine = sqlalchemy.create_engine('mysql://user:password@server') # connect to server
dbserver_engine = sqlalchemy.create_engine(DBserverURI) # connect to server
print('   dbserver_engine created')

print('  dbserver_engine.execute("CREATE DATABASE IF NOT EXISTS dbtest") #create db')
dbserver_engine.execute("CREATE DATABASE IF NOT EXISTS dbtest") #create db
print('  dbserver_engine.execute("USE dbtest')
dbserver_engine.execute("USE dbtest") # select new db
# use the new db
# continue with your work...
print('db created if NOT EXIT------------------')

#dbserver_engine.execute("CREATE DATABASE dbtest") #create db
#dbserver_engine.execute("USE dbtest") # select new db
# use the new db
# continue with your work...
#print('db created------------------')

# Query for existing databases
print('  dbserver_engine.execute("SHOW DATABASES;"')
existing_databases = dbserver_engine.execute("SHOW DATABASES;")
# Results are a list of single item tuples, so unpack each tuple
existing_databases = [d[0] for d in existing_databases]

# List databases
for database in existing_databases:
    print("database {0} exists on dbserver {1}".format(database,DBserverURI))

print('')
newdb='newdb'
# Create database if not exists
if newdb not in existing_databases:
    dbserver_engine.execute("CREATE DATABASE {0}".format(newdb))
    print("Created database {0} on DBserver {1}".format(newdb,DBserverURI))
else:
    print("database {0} already exists on DBserver {1}".format(newdb,DBserverURI))

print('')

# Go ahead and use this engine
# db_engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(user, pass, host, port, db))

print('')
database_username="root"
database_password="philea13"
#################################
#3: create database engine
#################################
DBURI = "{drivername}+{mysqlconnector}://{username}:{password}@{hostname}/{databasename}".format(
    drivername="mysql"
    ,mysqlconnector="pymysql"
    ,username="ganimedes"
    ,password="philea13"
    ,hostname="localhost" #, "ganimides.mysql.pythonanywhere-services.com",
    ,databasename="ganimedes_db"
)
print('DBURI =',DBURI)
localhost_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ganimedes:philea13@localhost/ganimedes_db'
print(localhost_SQLALCHEMY_DATABASE_URI)
print('------------------')

db_engine = sqlalchemy.create_engine(DBURI) # connect to database
print('   db_engine created')
# print(db_uri)
existing_tables = db_engine.execute('SHOW TABLES;')
# Results are a list of single item tuples, so unpack each tuple
existing_tables = [d[0] for d in existing_tables]

# List tables
for table in existing_databases:
    print("table {0} exists in database {1}".format(table,DBURI))

print('')


# engine = create_engine(db_uri)

# # # DBAPI - PEP249
# # # create table
# # engine.execute('CREATE TABLE "EX1" ('
# #                'id INTEGER NOT NULL,'
# #                'name VARCHAR, '
# #                'PRIMARY KEY (id));')
# # # insert a raw
# # engine.execute('INSERT INTO "EX1" '
# #                '(id, name) '
# #                'VALUES (1,"raw1")')

# # # select *
# # result = engine.execute('SELECT * FROM '
# #                         '"EX1"')
# # for _r in result:
# #    print(_r)

# # # delete *
# # engine.execute('DELETE from "EX1" where id=1;')
# # result = engine.execute('SELECT * FROM "EX1"')
# # print(result.fetchall())