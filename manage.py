from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from infrastructure.config.database_config import db
from infrastructure.config.flask import app

from domains.item.models.item import Item
from domains.item.models.item_ref import ItemRef
from domains.permission.models.permission import Permission
from domains.user.models.user import User

manager = Manager(app)
migrate = Migrate(app, db, render_as_batch=True, compare_type=True, compare_server_default=True)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()