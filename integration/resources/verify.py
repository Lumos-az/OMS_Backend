from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from common import code, pretty_result, gloVar
from models.user import UserModel, DocModel
from common.auth import create_login_token, verify_login_token
from models.BookingTime import BookingTimeModel
from sqlalchemy import or_,and_
from smtplib import SMTPDataError
from datetime import datetime
from flask_mail import Message


class Login(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('username', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['username'])
            if user is None or user.password != args['password']:
                return pretty_result(code.AUTHORIZATION_ERROR)
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
                'age': user.age,
                'sex': user.sex,
                'other': user.other,
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
                    'identity': user.utype,
                    'age': user.age,
                    'sex': user.sex,
                    'other': user.other,
                    'can_post': user.Can_post,
                    'can_reply': user.Can_reply
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


class ChangeRepoInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def put(self):
        print('111')
        self.parser.add_argument('user', type=str, location="args")
        self.parser.add_argument('identity', type=int, location="args")
        self.parser.add_argument('can_post', type=int, location="args")
        self.parser.add_argument('can_reply', type=int, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['user'])
            if args['identity'] != 5:
                user.utype = args['identity']
            user.Can_post = args['can_post']
            user.Can_reply = args['can_reply']
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CanPost(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('user', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['user'])
            data = user.Can_post
            return pretty_result(code.OK, data=data)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CanReply(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('user', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['user'])
            data = user.Can_reply
            return pretty_result(code.OK, data=data)

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
        self.parser.add_argument('registerType', type=str, location="args")
        self.parser.add_argument('proField', type=str, location="args")
        self.parser.add_argument('hospital', type=str, location="args")
        self.parser.add_argument('section', type=str, location="args")
        self.parser.add_argument('introduction', type=str, location="args")
        args = self.parser.parse_args()
        print(args)
        if len(args['uid']) != 18:
            return pretty_result(code.DB_ERROR, data="请输入正确的身份证号！")
        elif len(args['email']) == 0 or len(args['email']) >= 30:
            return pretty_result(code.DB_ERROR, data="邮箱长度必须大于0小于30")
        elif len(args['password']) < 6 or len(args['password']) >= 50:
            return pretty_result(code.DB_ERROR, data="密码长度必须大于等于6位，短于50位")
        elif len(args['nickname']) == 0 or len(args['nickname']) >= 50:
            return pretty_result(code.DB_ERROR, data="昵称长度必须大于0小于50")
        elif len(args['realName']) == 0 or len(args['realName']) >= 50:
            return pretty_result(code.DB_ERROR, data="真实姓名长度必须大于0小于50")
        elif len(args['phone']) == 0 or len(args['phone']) >= 20:
            return pretty_result(code.DB_ERROR, data="手机号长度必须大于0小于20")
        elif len(args['address']) == 0 or len(args['address']) >= 50:
            return pretty_result(code.DB_ERROR, data="居住地长度必须大于0小于50")
        elif args['sex'] != '男' and args['sex'] != '女':
            return pretty_result(code.DB_ERROR, data="请输入正确的性别")
        currentYear = datetime.now().year
        tmp = int(args['uid'][6:10])
        if str.isalpha(args['password']):
            return pretty_result(code.DB_ERROR, data="密码不能仅包含字母")
        elif str.isdigit(args['password']):
            return pretty_result(code.DB_ERROR, data="密码不能仅包含数字")
        elif not str.isdigit(args['phone']):
            return pretty_result(code.DB_ERROR, data="手机号码必须仅包含数字")
        user = UserModel(
            uid=args['uid'],
            password=args['password'],
            nickname=args['nickname'],
            name=args['realName'],
            address=args['address'],
            phoneNumber=args['phone'],
            emailAddr=args['email'],
            utype=0,
            age=currentYear - tmp,
            sex=args['sex'],
            other=args['other']
        )
        try:
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, data='该用户已存在')
        if args['registerType'] == 'doctor':
            try:
                doctmp = DocModel(
                    did=args['uid'],
                    profield=args['proField'],
                    hospital=args['hospital'],
                    room=args['section'],
                    introduction=args['introduction'],
                    activated=0
                )
                db.session.add(doctmp)
                db.session.commit()
            except SQLAlchemyError as e:
                print(e)
                db.session.rollback()
                return pretty_result(code.DB_ERROR, data='用户添加成功，医生添加失败')
            try:
                msg = Message(subject='医生账户注册说明', recipients=[args['email']])
                msg.body = args['realName'] + ',您好!:\n您的医生账户已经注册成功，请等待管理员审核，成功后会有进行邮件通知！'
                gloVar.get_value('mailData').send(msg)
                return pretty_result(code.OK, data='注册成功！')
            except SMTPDataError as e:
                print(e)
                return pretty_result(code.OTHER_ERROR)
        else:
            return pretty_result(code.OK)


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


class CanRegisterDoctor(Resource):
    def __init__(self):
        self.parser = RequestParser()

    @property
    def get(self):
        self.parser.add_argument('doctorid', type=int, location="args")
        self.parser.add_argument('timeid', type=int, location="args")
        args = self.parser.parse_args()

        try:
            bookingtime = BookingTimeModel.query.fliter(and_(BookingTimeModel.did==args['doctorid'],BookingTimeModel.did==args['doctorid']))
            data = bookingtime.isFull
            return pretty_result(code.OK, data=data)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class ReadUnactivatedDocs(Resource):
    def __init__(self):
        # 继承了Resource这个类，使用RequestParser这个函数，拦截下网页端发来的请求的内容
        self.parser = RequestParser()

    def get(self):
        try:
            docs = DocModel.query.all()
            if docs is None:
                return pretty_result(code.AUTHORIZATION_ERROR,data='医生用户尚不存在')

            data = []
            for doctor in docs:
                user = UserModel.query.get(doctor.did)
                if user is None:
                    return pretty_result(code.AUTHORIZATION_ERROR,data='后台数据库存在冲突无法加载')
                status = '未认证'
                if doctor.activated == 1:
                    status = '已认证'
                data.append({
                    'uid':doctor.did,
                    'name':user.name,
                    'proField':doctor.profield,
                    'hospital':doctor.hospital,
                    'room':doctor.room,
                    'identification':status
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class ActivateDocs(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        args = self.parser.parse_args()
        try:
            docotor = DocModel.query.get(args['uid'])
            docotor.activated = 1
            db.session.commit()

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR,data='医生激活失败')
        user = UserModel.query.get(args['uid'])
        try:
            user.utype = 1
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
        try:
            msg = Message(subject='医生账户激活结果',recipients=[user.emailAddr])
            msg.body = user.name + ',您好!:\n您的医生账户激活成功，欢迎您的加入！\n'
            gloVar.get_value('mailData').send(msg)
            return pretty_result(code.OK, data='激活成功')
        except SMTPDataError as e:
            print(e)
            return pretty_result(code.OTHER_ERROR)

    def delete(self):
        self.parser.add_argument('uid', type=str, location="args")
        args = self.parser.parse_args()
        user = UserModel.query.get(args['uid'])
        try:
            doc = DocModel.query.get(args['uid'])
            db.session.delete(doc)
            db.session.commit()

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR,data='医生激活失败')

        try:
            msg = Message(subject='医生账户变更',recipients=[user.emailAddr])
            msg.body = user.name + ',您好!:\n您的医生账户已失效'
            gloVar.get_value('mailData').send(msg)
            return pretty_result(code.OK, data='激活成功')
        except SMTPDataError as e:
            print(e)
            return pretty_result(code.OTHER_ERROR)


class DocIdentify(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('proField', type=str, location="args")
        self.parser.add_argument('hospital', type=str, location="args")
        self.parser.add_argument('room', type=str, location="args")
        self.parser.add_argument('introduction', type=str, location="args")
        args = self.parser.parse_args()
        print(args)
        user = UserModel.query.get(args['uid'])
        try:
            doctmp = DocModel(
                did=args['uid'],
                profield=args['proField'],
                hospital=args['hospital'],
                room=args['room'],
                introduction=args['introduction'],
                activated=0
            )
            db.session.add(doctmp)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, data='医生添加失败')
        try:
            msg = Message(subject='医生账户注册说明', recipients=[user.emailAddr])
            msg.body = user.name + ',您好!:\n您的医生账户已经申请成功，请等待管理员审核，成功后会有进行邮件通知！'
            gloVar.get_value('mailData').send(msg)
            return pretty_result(code.OK, data='注册成功！')
        except SMTPDataError as e:
            print(e)
            return pretty_result(code.OTHER_ERROR,data = '申请邮件发送失败')