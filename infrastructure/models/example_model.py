from sqlalchemy import Column, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'
    id = Column(INTEGER, primary_key=True)