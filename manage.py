from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from infrastructure.config.database_config import db
from infrastructure.config.flask import app

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()