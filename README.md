海马生鲜电商项目实战

零、后台管理模板编写和选择
从码云或者github去搜索想要的开源项目
vue lay-ui
Bootstrap 模板
一、部署Vue项目
使用npm run build打包，此时vue项目下会生成一个dist目录，dist目录下面是我们需要发布的代码
将dist目录下的代码复制到服务器
安装nginx yum install -y nginx
打开nginx的配置 vim /ect/nginx/nginx.conf

二、flask-script （python manager.py runserver）
安装：flask-script

初始化：

from flask_script import Manager

manager = Manager(app)
开启服务器

from flask_script import Server

manager.add_command( "runserver",Server(host="localhost",port=5000,use_debugger=True,use_reloader=True) )

manager.run()

三、Flask蓝图路由
蓝图的基本概念是：在蓝图被注册到应用之后，所要执行的操作的集合。当分配请求 时， Flask 会把蓝图和视图函数关联起来，并生成两个端点之前的 URL 。

/user_page/edit /user_page/add /user_page/delete

controllers

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
simple_page = Blueprint('simple_page', __name__,
                        template_folder='templates')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)


urls.py

from flask import Flask
from yourapplication.simple_page import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page, url_prefix='/pages')
实现普通用户模块

先实现C层：

引入flask的jsonfy模块

from flask import Blueprint,render_template,request,jsonify

@router_user.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('user/login.html')
    
    resp = {
        'code':200,
        'msg':'登录成功',
        'data':{}
    }
    print(request.values)
    return jsonify(resp)

四、url管理和面向对象复习
类的方法分几种：
普通方法：默认有self参数，只能够被对象调用
静态方法：@staticmethod 装饰，不带self参数，也可以没有参数，可以直接被类名调用
类方法：@classmethod 默认有一个cls参数，可以被类和对象调用
自定义一个UrlManager.py

import time

class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path
    
    @staticmethod
    def buildStaticUrl(path):
        ver = "%s"%(int(time.time()))
        path = "/static" + path + "?version=" + ver
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        pass 
	
要想在前端模板中使用python的对象或者方法，需要写成一个函数模板，注入到前端模板中

application.py

# 函数模板
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildUrl,'buildUrl')
app.add_template_global(UrlManager.buildStaticUrl,'buildStaticUrl')
app.add_template_global(UrlManager.buildImageUrl,'buildImageUrl')

五、创建user数据库
新建项目数据库：hmsc_db

create database `hmsc_db` default character set =`utf8`;
新建 user表

use hmsc_db;

drop table if exists `user`;
create table `user` (
	`uid` bigint(20) not null auto_increment comment '用户id',
	`nickname` varchar(100) not null default '' comment '用户昵称',
	`mobile` varchar(20) not null default '' comment '手机号码',
	`email` varchar(100) not null default '' comment '用户邮箱',
	`sex` tinyint(1) not null default '0' comment '1:男 2:女 0:没有填写',
	`avatar` varchar(64) not null default '' comment '头像',
	`login_name` varchar(20) not null default '' comment '登录用户名',
	`login_pwd` varchar(32) not null default '' comment '登录密码',
	`login_salt` varchar(32) not null default '' comment '登录密码的随机密钥',
	`status` tinyint(1) not null default '1' comment '1:有效 0:无效',
	`updated_time` timestamp not null default current_timestamp comment '最后一次更新时间',
	`created_time` timestamp not null default current_timestamp comment '创建时间',
	primary key (`uid`),
	unique key `login_name` (`login_name`)
)ENGINE=InnoDB default charset=utf8 comment='用户表（管理员）';



插入数据  login_name = Bruce   login_pwd = 123456
insert into `user` (`uid`,`nickname`,`mobile`,`email`,`sex`,`avatar`,`login_name`,`login_pwd`,`login_salt`,`status`,`updated_time`,`created_time`) values (1,'BruceNick','13933746521','Bruce@aliyun.com',1,'','Bruce','816440c40b7a9d55ff9eb7b20760862c','cF3JfH5FJfQ8B2Ba',1,'2020-04-23 11:30:30','2020-04-23 11:10:30');
使用flask-sqlacodegen 生成ORM model

安装 pip install flask-sqlacodegen

安装连接数据库的引擎 mysqlclient ( pymysql ) : pip install mysqlclient

安装flask-sqlalchemy

无密码单个表
flask-sqlacodegen 'mysql://root:@127.0.0.1/hmsc_db' --tables user --outfile "common/models/User.py" --flask
有密码单个表，密码是：123456
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables user --outfile "common/models/User.py" --flask 

flask-sqlacodegen 'mysql://root:@127.0.0.1/hmsc_db' --outfile "common/models/model.py" --flask

六、配置文件统一管理
从配置文件中加载配置

Application类中

self.config.from_pyfile('config/base_setting.py')
从其他配置文件加载，需要在运行项目之前，export ops_config=develop

if 'ops_config' in os.environ:
            self.config.from_pyfile("config/%s_setting.py"%os.environ['ops_config'])
        db.init_app(self)

七、结合MD5算法和密钥字符串生成密码
common/libs/user/UserService.py

import hashlib,base64
class UserService():
    
    # 结合salt和md5 生成新的密码
    @staticmethod
    def generatePwd(pwd,salt):
        m = hashlib.md5()
        str = "%s-%s"%(base64.encodebytes(pwd.encode("utf-8")),salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

八、登录登出逻辑
登录之后，把登录的状态做保持，session（服务端）和Cookie（客户端也就是浏览器上的）
我们使用客户端Cookie
判断Cookie 中的数据和数据库中的数据是否一致，如果一致且Cookie时间不过期，则表示已经登录
后台管理页面必须得有权限设置，必须得是登录之后才可以进入到其他页面

九、状态管理，将登陆状态记录到客户端Cookie中
(自行补充上session的状态管理)

from flask import make_response
import json


response = make_response(json.dumps({'code':200,'msg':'登录成功~~~'}))
# Cookie中存入的信息是uid
response.set_cookie("hmsc_1901C","信息",60*60*24*15)
return response
对Cookie中存储的信息进行加密 common/libs/user/UserService.py

# 对Cookie中存储的信息进行加密
    @staticmethod
    def generateAuthCode(user_info = None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

十、拦截器实现权限保护（类比watchlist中的@login_required）&&flask的g对象
拦截器逻辑 ：登录后，在去渲染首页之前，需要判断当前是否是登录状态，也就是cookie中的存储的信息是否和数据库中的一致，如果一致，则可以渲染首页，如果不一致，那返回登录页面

专门用来存储用户信息的g对象，全称叫做global，g对象在一次请求中的所有的代码的地方，都可以使用

所有的请求之前的拦截
@app.before_request
def before_request():
	pass
报错（原因：/user/login 进入死循环）

该网页无法正常运作localhost 将您重定向的次数过多。
尝试清除 Cookie.
ERR_TOO_MANY_REDIRECTS
解决办法，设置过滤规则

{{ current_user.nickname }} 'current_user' is undefined

是因为g对象的上下文context没有被渲染到模板中

十一、网站首页数据库设计
全站日统计
use hmsc_db;

drop table if exists `stat_daily_site`;

create table `stat_daily_site` (
    `id` int(11) unsigned not null auto_increment,
    `date` date not null comment '日期',
    `total_pay_money` decimal(10,2) not null default '0.00' comment '当日收入总额',
    `total_member_count` int(11) not null comment '会员总数',
    `total_new_member_count` int(11) not null comment '当日新增会员数',
    `total_order_count` int(11) not null comment '当日订单数',
    `total_shared_count` int(11) not null comment '分享总数',
    `updated_time` timestamp not null default current_timestamp comment '最近更新时间',
    `created_time` timestamp not null default current_timestamp comment '插入时间',
    primary key (`id`),
    key `idx_data` (`date`)
)engine=InnoDB default charset=utf8 comment='全站日统计';
生成models文件

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables stat_daily_site --outfile "common/models/stat/StatDailySite.py" --flask

十二、 account 模块
路由 http://localhost:9000/account/info?id=1 中取出id

request.args.get('id')

request.args.get('id') 路由中有时带id参数，有时又不带，不带的话就为id空了，通过int()强制类型转换的时候，就会报错

int() argument must be a string, a bytes-like object or a number, not 'NoneType'
所以必须提供一个默认参数 0， uid = int(req.get("id",0))

搜索

from sqlalchemy import or_

或者

分页

关键字：当前页（计算出从第几个元素开始），每页显示多少（page_size），一共多少页（pages）

总的查询结果数  total = User.query.count()
每页显示多少个数据   page_size = 5
当前页  page
url  http://localhost:8999/account/index&p=1
计算出来的
pages_total  总共有多少页  total/page_size
当前页数据开始位置  offset = (page-1) * page_size
当前页数据结束位置  limit = page * page_size

十三、member 会员管理
一、会员账号 数据库
会员账号 数据库
use hmsc_db;

drop table if exists `member`;
create table `member` (
	`id` int(11) unsigned not null auto_increment,
	`nickname` varchar(100) not null default '' comment '会员昵称',
	`mobile` varchar(20) not null default '' comment '会员手机号码',
	`sex` tinyint(1) not null default '0' comment '1:男 2:女 0:没有填写',
	`avatar` varchar(200) not null default '' comment '会员头像',
	`salt` varchar(32) not null default '' comment '登录密码的随机密钥',
	`reg_ip` varchar(100) not null default '' comment '注册ip',
	`status` tinyint(1) not null default '1' comment '1:有效 0:无效',
	`updated_time` timestamp not null default current_timestamp comment '最后一次更新时间',
	`created_time` timestamp not null default current_timestamp comment '创建时间',
	primary key (`id`)
)ENGINE=InnoDB default charset=utf8 comment='会员表';
生成models

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables member --outfile "common/models/member/Member.py" --flask
插入数据

insert into `member` (`id`,`nickname`,`mobile`,`sex`,`avatar`,`salt`,`reg_ip`,`status`,`updated_time`,`created_time`) values (1,'BruceNick','13933746521',1,'','cF3JfH5FJfQ8B2Ba','20200429',1,'2020-04-29 11:30:30','2020-04-29 11:10:30');
二、会员评论 数据库
会员评论 数据库

use hmsc_db;

drop table if exists `member_comments`;
create table `member_comments`(
	`id` int(11) unsigned not null auto_increment,
	`member_id` int(11) not null default '0' comment '会员id',
	`goods_id` varchar(200) not null default '' comment '商品id',
	`pay_order_id` int(11) not null default '0' comment '订单id',
	`score` tinyint(4) not null default '0' comment '评分',
	`content` varchar(200) not null default '' comment '评论内容',
	`created_time` timestamp not null default current_timestamp on update current_timestamp comment '创建时间',
	primary key (`id`),
	key `idx_member_id` (`member_id`)
)ENGINE=InnoDB default charset=utf8 comment='会员评论表';
生成model

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables member_comments --outfile "common/models/member/MemberComment.py" --flask
插入数据

insert into `member_comments` (`id`,`member_id`,`goods_id`,`pay_order_id`,`score`,`content`,`created_time`) values (1,1,'1',1,'10','好，good','2020-04-29 11:10:30');

十四、商品管理 goods
数据库

use hmsc_db;

drop table if exists `goods`;
create table `goods` (
    `id` int(11) unsigned not null auto_increment,
    `cat_id` int(11) not null default '0' comment '分类id',
    `name` varchar(100) not null default '' comment '商品名称',
    `price` decimal(10,2) not null default '0.00' comment '商品价格',
    `main_image` varchar(100) not null default '' comment '商品主图',
    `summary` varchar(10000) not null default '' comment '商品描述',
    `stock` int(11) not null default '0' comment '库存数',
    `tags` varchar(200) not null default '' comment 'tag 标签，用“,”连接',
    `status` tinyint(1) not null default '1' comment '1:有效，0：无效',
    `month_count` int(11) not null default '0' comment '月销量',
    `total_count` int(11) not null default '0' comment '总销量',
    `view_count` int(11) not null default '0' comment '总浏览次数',
    `comment_count` int(11) not null default '0' comment '总评论数',
    `updated_time` timestamp not null default current_timestamp comment '最后一次更新时间',
	`created_time` timestamp not null default current_timestamp comment '创建时间',
	primary key (`id`)
)ENGINE=InnoDB default charset=utf8 comment='商品表';
生成models

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables goods --outfile "common/models/goods/Goods.py" --flask
插入数据

insert into `member_comments` (`id`,`member_id`,`goods_id`,`pay_order_id`,`score`,`content`,`created_time`) values (1,1,'1',1,'10','好，good','2020-04-29 11:10:30');

十五、集成UEditor和HighCharts
一、UEditor
官网：http://ueditor.baidu.com/website/ 看文档

在Flask项目中集成UEditor：https://segmentfault.com/a/1190000002429055/

加载UEditor后端配置，json格式，

上传图片：

上传图片后，图片在服务器上的地址 /web/static/upload/20200430/avatar.jpg

图片在前端img标签中的src中的地址

服务器图片加密存储 UUID 16进制 32位的一串字符串，基于随机数

import uuid

二、Highcharts