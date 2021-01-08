
from flask_sqlalchemy import SQLAlchemy

from infrastructure.config.flask import app

db = SQLAlchemy(app)
db_session = db.session
