from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.reply import ReplyModel, ReplyReportModel
from models.user import UserModel
from common import code, pretty_result, file
from werkzeug.datastructures import FileStorage


class Replies(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, post_id):
        try:
            data = []
            replies = ReplyModel.query.filter_by(Belong_Post_id=post_id).all()
            for reply in replies:
                if reply.file is not None:
                    has_file = True
                else:
                    has_file = False
                identity = UserModel.query.get(reply.Author_id)
                data.append({
                    'reply_id': reply.Reply_id,
                    'user_id': identity.nickname,
                    'time': str(reply.Date),
                    'content': reply.Content,
                    'user_identity': identity.uid,
                    'file': 'file/reply/' + str(reply.Reply_id),
                    'has_file': has_file
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
            self.parser.add_argument('file', type=FileStorage, location='files')
            args = self.parser.parse_args()

            reply = ReplyModel(
                Belong_Post_id=post_id,
                Content=args['content'],
                Author_id=args['user_id']
            )
            db.session.add(reply)
            db.session.commit()
            file.upload_resource_reply(args['file'], reply)
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
            reply = ReplyModel.query.get(reply_id)
            file.delete_resource_reply(reply)
            db.session.delete(reply)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Reply_Report(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        try:
            reports = ReplyReportModel.query.all()
            data = []
            for report in reports:
                reply = ReplyModel.query.get(report.reply_id)
                data.append({
                    'id': report.report_id,
                    'reporter_id': report.reporter_id,
                    'content': report.content,
                    'author_id': reply.Author_id,
                    'reply_content': reply.Content,
                    'reply_id': report.reply_id
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self):
        try:
            self.parser.add_argument('reply_id', type=int, location='args')
            self.parser.add_argument('reporter_id', type=str, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()
            report = ReplyReportModel(
                reply_id=args['reply_id'],
                reporter_id=args['reporter_id'],
                content=args['content']
            )
            db.session.add(report)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self):
        try:
            self.parser.add_argument('report_id', type=int, location='args')
            args = self.parser.parse_args()
            report = ReplyReportModel.query.get(args['report_id'])
            db.session.delete(report)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)