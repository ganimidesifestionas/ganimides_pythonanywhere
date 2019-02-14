#encoding: utf-8
import os
#from flask.ext.script import Manager
#from flask.ext.migrate import Migrate, MigrateCommand
import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from website_app import db
from website_app import app as application
from website_app.module_administration.models import User, Department, Role
from website_app.module_authorization.models import Subscriber, ContactMessage
from website_app.models import Visit, VisitPoint, Page_Visit

app = application
app.app_context().push()
DATABASE_SERVER = app.config['DATABASE_SERVER']
DATABASE_SERVER_URI = app.config['DATABASE_SERVER_URI']
DATABASE_NAME = app.config['DATABASE_NAME']
DATABASE_URI = app.config['DATABASE_URI']
#from start_server import app
#from myApp import db
#from myApp.module_home.models import Subscriber,User
#from app import app, db
#app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# def migrate_database():
#     print(__name__, '######################################################')
#     migrate = Migrate(app, db)
#     manager = Manager(app)
#     manager.add_command('db', MigrateCommand)
#     manager.run()
#     print(__name__, '######################################################')

if __name__ == '__main__':
    manager.run()

@manager.command
def create_admin():
    """Creates the admin user."""
    dbadmin_user = User(
    email="ganimedesifestionas@outlook.com"
    ) 
    db.session.add(dbadmin_user)
    db.session.commit()
