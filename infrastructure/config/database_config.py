
from flask_sqlalchemy import SQLAlchemy

from infrastructure.config.flask import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost:3306/rbac?auth_plugin=mysql_native_password'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db_session = db.session
