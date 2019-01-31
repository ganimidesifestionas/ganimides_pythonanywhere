from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#DATABASE_SERVER = app.config['DATABASE_SERVER']
#DATABASE_SERVER_URI = app.config['DATABASE_SERVER_URI']
#DATABASE_NAME = app.config['DATABASE_NAME']
#DATABASE_URI = app.config['DATABASE_URI']
DATABASE_URI = 'mysql+pymysql://root:philea13@localhost/ganimedes_db_test'

engine = create_engine(DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    