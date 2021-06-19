from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from werkzeug.exceptions import UnsupportedMediaType
from datetime import datetime
from models import db
from common import code, pretty_result
from models.user import UserModel
from common.auth import create_login_token, verify_login_token


class Login(Resource):
    def __init__(self):
        # 继承了Resource这个类，使用RequestParser这个函数，拦截下网页端发来的请求的内容
        self.parser = RequestParser()

    def get(self):
        #虽然不理解细节，但是应该是把网页端传递过来的username和password截下放到args
        self.parser.add_argument('username', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        args = self.parser.parse_args()

        try:
            #锁定在userinfo表上
            user = UserModel.query.get(args['username'])
            #if判断，错误就退出，正确就继续
            if user is None or user.password != args['password']:
                return pretty_result(code.AUTHORIZATION_ERROR)
            #调用了auth.py中创建的函数创建了令牌
            token = str(create_login_token({
                'status': 'login',
                'username': user.uid,
            }), encoding='utf-8')
            data = {
                'token': token,
                'identity': user.utype,
                'nickname': user.nickname,
                'email': user.emailAddr,
                'phone': user.phoneNumber,
                'address': user.address,
                'age':user.age,
                'sex':user.sex,
                'other':user.other,
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class IsLogin(Resource):
    def __init__(self):
        self.token_parser = RequestParser()

    def post(self):
        if verify_login_token(self.token_parser) is False:
            print(pretty_result(code.AUTHORIZATION_ERROR))
            return pretty_result(code.AUTHORIZATION_ERROR)
        else:
            print(pretty_result(code.OK))
            return pretty_result(code.OK)


class GetUsers(Resource):
    def __init__(self):
        self.token_parser = RequestParser()

    def get(self):
        try:
            users = UserModel.query.all()
            data = []
            for user in users:
                data.append({
                    'uid': user.uid,
                    'nickname': user.nickname,
                    'name': user.name,
                    'address': user.address,
                    'phoneNumber': user.phoneNumber,
                    'age': user.age,
                    'sex': user.sex,
                    'other':user.other
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ChangeInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def put(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('nickname', type=str, location="args")
        self.parser.add_argument('address', type=str, location="args")
        self.parser.add_argument('phone', type=str, location="args")
        self.parser.add_argument('email', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['uid'])
            user.nickname = args['nickname']
            user.address = args['phone']
            user.emailAddr = args['email']
            user.address = args['address']
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class RegisterUser(Resource):
    def __init__(self):
        self.parser = RequestParser()
        
    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('email', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        self.parser.add_argument('nickname', type=str, location="args")
        self.parser.add_argument('realName', type=str, location="args")
        self.parser.add_argument('address', type=str, location="args")
        self.parser.add_argument('phone', type=str, location="args")
        self.parser.add_argument('sex', type=str, location="args")
        self.parser.add_argument('other', type=str, location="args")
        args = self.parser.parse_args()
        print(args)
        if len(args['uid'])!= 18:   
            return pretty_result(code.DB_ERROR,data="请输入正确的身份证号！")
        elif len(args['email']) == 0 or len(args['email']) >= 30:
            return pretty_result(code.DB_ERROR,data="邮箱长度必须大于0小于30")
        elif len(args['password']) < 6 or len(args['password']) >= 50:
            return pretty_result(code.DB_ERROR,data="密码长度必须大于等于6位，短于50位")
        elif len(args['nickname']) == 0 or len(args['nickname']) >= 50:
            return pretty_result(code.DB_ERROR,data="昵称长度必须大于0小于50")
        elif len(args['realName']) == 0 or len(args['realName']) >= 50:
            return pretty_result(code.DB_ERROR,data="真实姓名长度必须大于0小于50")
        elif len(args['phone']) == 0 or len(args['phone']) >= 20:
            return pretty_result(code.DB_ERROR,data="手机号长度必须大于0小于20")
        elif len(args['address']) == 0 or len(args['address']) >= 50:
            return pretty_result(code.DB_ERROR,data="居住地长度必须大于0小于50")
        elif args['sex'] != '男' and args['sex'] != '女':
            return pretty_result(code.DB_ERROR,data="请输入正确的性别")
        currentYear = datetime.now().year
        tmp = int(args['uid'][6:10])
        if str.isalpha(args['password']):
            return pretty_result(code.DB_ERROR,data="密码不能仅包含字母")
        elif str.isdigit(args['password']):
            return pretty_result(code.DB_ERROR,data="密码不能仅包含数字")

        user = UserModel(
            uid=args['uid'],
            password=args['password'],
            nickname=args['nickname'],
            name=args['realName'],
            address=args['address'],
            phoneNumber=args['phone'],
            emailAddr=args['email'],
            utype=0,
            age = currentYear - tmp,
            sex = args['sex'],
            other = args['other']
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class ChangeCode(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('oldPassword', type=str, location="args")
        #self.parser.add_argument('address', type=int, location="args")
        self.parser.add_argument('newPassword', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['uid'])
            if user is None or user.password != args['oldPassword']:
                print(args['oldPassword'])
                return pretty_result(code.DB_ERROR,data = "原密码错误，请输入正确密码！")
            elif len(args['newPassword']) < 6 or len(args['newPassword']) > 50:
                return pretty_result(code.DB_ERROR,data = "密码长度应在6位和50位之间")
            elif user.password == args['newPassword']:
                return pretty_result(code.DB_ERROR,data = "新旧密码不能相同")
            user.password = args['newPassword']
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
