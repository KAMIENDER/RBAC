from sqlalchemy import Column, INTEGER, VARCHAR, UniqueConstraint

from infrastructure.config.database_config import db


class Item(db.Model):
    __tablename__ = 'item'
    id = Column(INTEGER, primary_key=True)
    type = Column(INTEGER, nullable=False)
    disable = Column(INTEGER, nullable=False, default=0)
    key = Column(VARCHAR(255), nullable=False)
    extra = Column(VARCHAR(255))

    __table_args__ = (
        UniqueConstraint('key', 'type'),  # 姓名和年龄唯一
    )