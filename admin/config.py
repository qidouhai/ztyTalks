# encoding: utf-8

DIALECT = 'mysql'  # 要用的什么数据库
DRIVER = 'pymysql'  # 连接数据库驱动
USERNAME = 'talks'  # 用户名
PASSWORD = '*********'  # 密码
HOST = '127.0.0.1'  # 服务器
PORT = '3306'  # 端口
DATABASE = 'talks'  # 数据库名
DATABASE2 = 'bbq'  # 数据库名


SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)

SQLALCHEMY_BINDS = {
    'bbq': "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                        DATABASE2)  # 另外配置的数据库
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 8
