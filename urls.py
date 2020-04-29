from application import app
from web.controllers.user.User import route_user
from web.controllers.index import route_index
from web.controllers.account.Account import route_account
from web.controllers.member.Member import route_member
# 拦截器的路由
from web.interceptos.AuthInterceptor import *


# 蓝图路由
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_index,url_prefix='/')
app.register_blueprint(route_account,url_prefix='/account')
app.register_blueprint(route_member,url_prefix='/member')