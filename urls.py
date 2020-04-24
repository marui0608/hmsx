from application import app
from web.controllers.user.User import route_user
from web.controllers.index import route_index

# 拦截器的路由
from web.interceptos.AuthInterceptor import *


# 蓝图路由
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_index,url_prefix='/')