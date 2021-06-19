from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.reply import ReplyModel
from models.user import UserModel
from common import code, pretty_result


class Replies(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, post_id):
        try:
            data = []
            replies = ReplyModel.query.filter_by(Belong_Post_id=post_id).all()
            for reply in replies:
                identity = UserModel.query.get
                data.append({
                    'reply_id': reply.Reply_id,
                    'user_id': reply.Author_id,
                    'time': str(reply.Date),
                    'content': reply.Content,
                    'user_identity': identity.identity
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, post_id):
        try:
            self.parser.add_argument('user_id', type=str, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()

            reply = ReplyModel(
                Belong_Post_id=post_id,
                Content=args['content'],
                Author_id=args['user_id']
            )
            db.session.add(reply)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Reply(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def delete(self, reply_id):
        try:
            reply = ReplyModel.query.get
            db.session.delete(reply)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
