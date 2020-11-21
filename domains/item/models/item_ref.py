from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ItemRef(Base):
    # 记录的是从属关系，attach为从，main为主
    __tablename__ = 'item_ref'
    id = Column(INTEGER, primary_key=True)
    main_id = Column(INTEGER, nullable=False)
    attach_id = Column(INTEGER, nullable=False)
    disable = Column(INTEGER, nullable=False)
    extra = Column(VARCHAR(255))
