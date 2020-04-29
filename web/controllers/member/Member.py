from flask import Blueprint,request,redirect,jsonify
from sqlalchemy import or_

from common.libs.Helper import ops_render,getCurrentDate,iPagenation
from common.models.Member import Member
from common.models.MemberComment import MemberComment
from application import db,app

route_member = Blueprint("member_page",__name__)

@route_member.route("/index")
def index():
    resp_data = {}
    query = Member.query
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))
    if 'mix_kw' in req:
        rule = or_(Member.nickname.ilike("%{0}%".format(req['mix_kw'])),Member.mobile.like("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    params = {
        "total": query.count(),
        "page_size": 5,
        "page": page,
        "url": request.full_path.replace("&p={}".format(page),"")
    }
    pages = iPagenation(params)
    # 当前页数据开始位置
    offset = (page-1) * 5
    # 当前页数据世杰位置
    limit = page * 5

    list = query.all()[offset:limit]

    resp_data['list'] = list
    resp_data['status'] = app.config['STATUS']
    resp_data['pages'] = pages

    return ops_render("member/index.html",resp_data)

@route_member.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get('id',0)) if req['id'] else 1
    member_info = Member.query.filter_by(id=id).first()
    resp_data['info'] = member_info
    return ops_render("member/info.html",resp_data)

@route_member.route("/set",methods=['GET','POST'])
def set():
    resp_data = {}
    req = request.args
    id = int(req.get('id',0)) if req['id'] else 1
    member_info = Member.query.filter_by(id=id).first()
    resp_data['info'] = member_info
    return ops_render("member/set.html",resp_data)

@route_member.route("/comment")
def comment():
    resp_data = {}
    comment_list = MemberComment.query.all()
    resp_data['list'] = comment_list
    member_info = {
        'avatar':'',
        'nickname':'Mary'
    }
    for item in comment_list:
        item.member_info = member_info
    return ops_render("member/comment.html",resp_data)

@route_member.route("/remove-or-recover",methods=['POST','GET'])
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

    member_info = Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "该账号不存在"
        return jsonify(resp)

    if acts == 'remove':
        member_info.status = 0
    elif acts == 'recover':
        member_info.status = 1
    
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()

    return jsonify(resp)