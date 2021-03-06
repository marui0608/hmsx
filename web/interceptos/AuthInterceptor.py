from flask import request,redirect,g

from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from application import app
from common.models.User import User
import re


# 每次请求之前都要先经过这里
@app.before_request
def before_request():
    path = request.path
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config["IGNORE_CHECK_LOGIN_URLS"]
    print(path)
    # 设置忽略静态资源 ^/static
    pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    user_info = check_login()
    # 判断
    g.current_user = None
    if user_info:
        g.current_user = user_info

    # 设置/user/login的忽略规则,需要用到正则表达式 ^/user/login
    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info:
        return redirect(UrlManager.buildUrl('/user/login'))
    return

# 判断用户是否登录,返回用户信息 user_info
def check_login():
    cookies = request.cookies
    auth_cookie = cookies[app.config["AUTH_COOKIE_NAME"]] if app.config["AUTH_COOKIE_NAME"] in cookies else None

    if auth_cookie is None:
        return False
    # 取出uid
    auth_info = auth_cookie.split("@")
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if auth_info[0] != UserService.generateAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
