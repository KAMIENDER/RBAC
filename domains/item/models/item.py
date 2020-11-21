from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = 'item'
    id = Column(INTEGER, primary_key=True)
    type = Column(INTEGER, nullable=False)
    disable = Column(INTEGER, nullable=False, default=0)
    key = Column(VARCHAR(255), nullable=False)
    extra = Column(VARCHAR(255))