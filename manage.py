#encoding: utf-8
import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from start_server import app
from myApp import db
from myApp.module_home.models import Subscriber,User

manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User(
        email="ganimedesifestionas@outlook.com",
        password="philea13",
        isAdmin=True,
        confirmed=True,
        confirmedDT=datetime.datetime.now())
    )
    db.session.commit()