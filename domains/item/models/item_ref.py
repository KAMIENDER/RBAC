from sqlalchemy import Column, INTEGER, VARCHAR

from infrastructure.config.database_config import db


class ItemRef(db.Model):
    # 记录的是从属关系，attach为从，main为主
    __tablename__ = 'item_ref'
    id = Column(INTEGER, primary_key=True)
    main_id = Column(INTEGER, nullable=False)
    attach_id = Column(INTEGER, nullable=False)
    disable = Column(INTEGER, nullable=False)
    extra = Column(VARCHAR(255))
