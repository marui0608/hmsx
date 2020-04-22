from application import app
from web.controllers.user.User import route_user

app.register_blueprint(route_user,url_prefix="/user")