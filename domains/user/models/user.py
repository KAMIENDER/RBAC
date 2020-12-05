from sqlalchemy import Column, INTEGER, VARCHAR

from infrastructure.config.database_config import db


class User(db.Model):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    type = Column(INTEGER, nullable=False)
    phone = Column(INTEGER, nullable=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=True)
    disable = Column(INTEGER, nullable=False)
    level = Column(INTEGER, nullable=False)
    key = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)

