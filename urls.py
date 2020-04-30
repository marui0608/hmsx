from application import app
from web.controllers.user.User import route_user
from web.controllers.index import route_index
from web.controllers.account.Account import route_account
from web.controllers.member.Member import route_member
from web.controllers.goods.Goods import route_goods
from web.controllers.upload.Upload import route_upload
# 拦截器的路由
from web.interceptos.AuthInterceptor import *


# 蓝图路由
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_index,url_prefix='/')
app.register_blueprint(route_account,url_prefix='/account')
app.register_blueprint(route_member,url_prefix='/member')
app.register_blueprint(route_goods,url_prefix='/goods')
app.register_blueprint(route_upload,url_prefix='/upload')