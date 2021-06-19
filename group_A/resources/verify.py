from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from common import code, pretty_result
from models.user import UserModel
from models.BookingTime import BookingTimeModel
from common.auth import create_login_token, verify_login_token
from sqlalchemy import or_,and_

class Login(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('username', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get
            if user is None or user.password != args['password']:
                return pretty_result(code.AUTHORIZATION_ERROR)
            token = str(create_login_token({
                'status': 'login',
                'username': user.id,
            }), encoding='utf-8')
            data = {
                'token': token,
                'identity': user.identity,
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
                    'name': user.id,
                    'identity': user.identity,
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
        self.parser.add_argument('user', type=str, location="args")
        self.parser.add_argument('identity', type=int, location="args")
        self.parser.add_argument('can_post', type=int, location="args")
        self.parser.add_argument('can_reply', type=int, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get
            user.identity = args['identity']
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
            user = UserModel.query.get
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
            user = UserModel.query.get
            data = user.Can_reply
            return pretty_result(code.OK, data=data)

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
