from sqlalchemy import Column, INTEGER, VARCHAR, UniqueConstraint, DateTime

from infrastructure.config.database_config import db


class Role(db.Model):
    __tablename__ = 'role'
    id = Column(INTEGER, primary_key=True)
    type = Column(INTEGER, nullable=False)
    disable = Column(INTEGER, nullable=False, default=0)
    key = Column(VARCHAR(255), nullable=False, unique=True)
    extra = Column(VARCHAR(255))
    name = Column(VARCHAR(255), nullable=False)
    level = Column(INTEGER, nullable=False)
    modifiedtime = Column(DateTime, nullable=False)

