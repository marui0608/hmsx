from flask import Blueprint,render_template,jsonify,request,make_response,g,redirect

from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.Helper import ops_render
from application import app,db

import json

route_user = Blueprint('user_page',__name__)

@route_user.route("/login",methods=['POST','GET'])
def login():
    if request.method == "GET":
        if g.current_user:
            return redirect(UrlManager.buildUrl("/"))
        return ops_render("user/login.html")

    resp = {
        'code':200,
        'msg':'登录成功！',
        'data':{}
    }
    req = request.values
    print(req)
    login_name = req['login_name']
    login_pwd = req['login_pwd']
    # 后端校检  不为空  长度不小于1
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入正确的用户名~~~"
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入正确的密码~~~"
        return jsonify(resp)

    # 数据库比对
    user_info = User.query.filter_by(login_name=login_name).first()
    print(user_info.login_pwd)
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '用户不存在'
        return jsonify(resp)
    if user_info.status != 1:
        resp['code'] = -1
        resp['msg'] = '账号已被禁用，请联系管理员处理'
        return jsonify(resp)
    if user_info.login_pwd != UserService.generatePwd(login_pwd,user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = "密码错误!"
        return jsonify(resp)

    # 将用户信息存入到浏览器的Cookie中
    # json.dumps() 只能处理 dict，list类型；经过处理的后的类型可以直接在浏览器中使用
    response = make_response(json.dumps({
        'code':200,
        'msg':'登陆成功！'
    }))
    # name:名字   value：内容  time：过期时间 
    # value 包括 login_name  login_pwd login_salt  uid
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],'%s@%s'%(UserService.generateAuthCode(user_info),user_info.uid),60*60*24*5)
    
    return response
    
    # return jsonify(resp)

@route_user.route("/edit",methods=['GET','POST'])
def edit():
    if request.method == "GET":
        return ops_render("/user/edit.html")
    # POST
    resp = {
        "code":200,
        "msg":"编辑成功",
        "data":{}
    }

    # 获取到值
    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    # 校检
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的nickname"
        return jsonify(resp)
    
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的email"
        return jsonify(resp)
        
    # 更新数据库的操作
    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)


@route_user.route("/reset-pwd",methods=['GET','POST'])
def resetPwd():
    if request.method == "GET":
        return ops_render("/user/reset_pwd.html")
    
    # POST
    resp = {
        "code":200,
        "msg":"重置密码成功",
        "data":{}
    }

    
    req = request.values
    old_password = req['old_password'] if "old_password" in req else ''
    new_password = req['new_password'] if "new_password" in req else ''
    print(old_password)
    print(new_password)
    # 校检
    # 旧密码
    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原始密码"
        return jsonify(resp)
    # 新密码
    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码"
        return jsonify(resp)
    # 旧密码和新密码是否一致
    if new_password == old_password:
        resp['code'] = -1
        resp['msg'] = "请输入与原始密码不相同的新密码"
        return jsonify(resp)
    # 重新给密码加密
        # 获取用户信息，修改密码为新密码生成的加密密码
    user_info = g.current_user
    # 设置缓存
    user_info.login_pwd = UserService.generatePwd(new_password,user_info.login_salt)
    # 添加到数据库，作为更改
    db.session.add(user_info)
    db.session.commit()

    # 更新cookie中的旧密码
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],"%s@%s" % (UserService.generateAuthCode(user_info),user_info.uid),60*60*24*5)

    return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response