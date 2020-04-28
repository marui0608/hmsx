from flask import Blueprint,request,redirect,jsonify

from common.libs.Helper import ops_render,getCurrentDate
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User
from application import db

route_account = Blueprint("account_page",__name__)

@route_account.route("/index")
def index():
    resp_data = {}
    list = User.query.all()
    resp_data['list'] = list
    return ops_render("/account/index.html",resp_data)

@route_account.route("/info")
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get("id",0))  # 路由后面没有id的时候，使用int()强制转换类型  默认值为0
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect(reback_url)
    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(reback_url)
    resp_data['info'] = info
    return ops_render("/account/info.html",resp_data)


'''
    路由带ID参数，就是修改：更新数据库
    路由不带ID参数，就是添加：创建数据，插入数据库
'''
@route_account.route("/set",methods=['POST','GET'])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id",0))
        info = None
        if uid:
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render("/account/set.html",resp_data)
    
    # POST
    resp = {
        'code':200,
        'msg':'操作成功',
        'data':{}
    }

    # 获取前端ajax传递的data
    req = request.values
    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else 0
    mobile = req['mobile'] if 'mobile' in req else 0
    email = req['email'] if 'email' in req else 0
    login_name = req['login_name'] if 'login_name' in req else 0
    login_pwd = req['login_pwd'] if 'login_pwd' in req else 0

    # 校检
    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的nickname"
        return jsonify(resp)
    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的mobile"
        return jsonify(resp)
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的email"
        return jsonify(resp)
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的login_name"
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的login_pwd"
        return jsonify(resp)
        
    # 筛选
    is_exits = User.query.filter(User.login_name == login_name,User.uid != id).first()
    if is_exits:
        resp['code'] = -1
        resp['msg'] = "改登录名已经存在，请更换"
        return jsonify(resp)

    
    user_info = User.query.filter_by(uid=id).first()

    if user_info:
        model_user = user_info
    else:
        model_user = User()
        # 插入格式化的时间
        model_user.create_time = getCurrentDate()
        # 生成十六位的加密字符串
        model_user.login_salt = UserService.generateSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    
    if user_info and user_info == 1:
        resp['code'] = -1
        resp['msg'] = "该用户为Mary"
        return jsonify(resp)

    model_user.login_pwd = UserService.generatePwd(login_pwd,model_user.login_salt)
    # 插入格式化的时间
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()

    return jsonify(resp)



@route_account.route("/remove-or-recover",methods=['POST','GET'])
def removeOrRecover():
    resp = {
        'code':200,
        'msg':"操作成功",
        "data":{}
    }

    req = request.values
    id = req['id'] if 'id' in req else 0
    acts = req['acts'] if 'acts' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
        return jsonify(resp)
    if acts not in ['remove','recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "该账号不存在"
        return jsonify(resp)

    if user_info and user_info.uid == 1:
        resp['code'] = -1
        resp['msg'] = "该账号是Mary，不允许操作"
        return jsonify(resp)

    if acts == 'remove':
        user_info.status = 0
    elif acts == 'recover':
        user_info.status = 1
    
    user_info.updated_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)