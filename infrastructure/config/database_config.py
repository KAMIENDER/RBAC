from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/rbac?auth_plugin=mysql_native_password')
session = sessionmaker(bind=engine)
db_session = session()
