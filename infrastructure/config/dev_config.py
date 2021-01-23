# basic config
DEBUG = True

# redis config
REDIS_URL = "redis://:@localhost:6379/0"

# database config
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@localhost:3306/rbac?auth_plugin=mysql_native_password"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
