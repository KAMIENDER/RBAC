from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    type = Column(INTEGER, nullable=False)
    phone = Column(INTEGER)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255))
    disable = Column(INTEGER)
    level = Column(INTEGER, nullable=False)
    key = Column(VARCHAR(255), nullable=False)

