USER="my_framework_user"
PASSWORD="password"
HOST="localhost"
PORT="3306"
NAME="my_framework_db"

SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(USER, PASSWORD, HOST, NAME)
