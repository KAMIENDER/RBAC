from sqlalchemy import Column, INTEGER, VARCHAR

from infrastructure.config.database_config import db


class Permission(db.Model):
    __tablename__ = 'permission'
    id = Column(INTEGER, primary_key=True)
    disable = Column(INTEGER, nullable=False, default=0)
    key = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(255), nullable=False)
    level = Column(INTEGER, nullable=False, default=0)
    extra = Column(VARCHAR(255))