# 设置服务器端口
SERVER_PORT = 8999
# 连接到数据库
SQLALCHEMY_DATABASE_URI = 'mysql://root:ma060800@127.0.0.1/hmsx_db?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 自动登录的 cookie
AUTH_COOKIE_NAME = 'Mary_hmsx'


# 拦截器忽略规则
IGNORE_URLS = ["^/user/login"]
IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
    # "^/images"
]

# 
STATUS = {
    "1":"正常",
    "0":"已删除",
}