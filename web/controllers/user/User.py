from flask import Blueprint,render_template,jsonify,request


route_user = Blueprint('user_page',__name__)

@route_user.route("/login",methods=['POST','GET'])
def login():
    
    return render_template("user/login.html")


@route_user.route("/loginout")
def loginout():
    return "loginout 页面"


@route_user.route("/edit")
def edit():
    return "编辑页面"


@route_user.route("/rest-pwd")
def restPwd():
    return "重置密码页面"