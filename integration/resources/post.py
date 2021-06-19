from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.post import PostModel, PostReportModel
from models.user import UserModel
from models.reply import ReplyModel
from common import code, pretty_result, file
from werkzeug.datastructures import FileStorage


class Posts(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            topposts = PostModel.query.filter_by(Type=1).all()
            posts = PostModel.query.filter_by(Type=0).all()
            for post in topposts:
                nickname = UserModel.query.get(post.Author_id).nickname
                data.append({
                    'post_id': post.Post_id,
                    'user_id': nickname,
                    'time': str(post.Date),
                    'title': post.Title,
                    'content': post.Content,
                    'type': post.Type
                })
            for post in posts:
                nickname = UserModel.query.get(post.Author_id).nickname
                data.append({
                    'post_id': post.Post_id,
                    'user_id': nickname,
                    'time': str(post.Date),
                    'title': post.Title,
                    'content': post.Content,
                    'type': post.Type
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self):
        try:
            self.parser.add_argument('user_id', type=str, location='args')
            self.parser.add_argument('title', type=str, location='args')
            self.parser.add_argument('content', type=str, location='args')
            self.parser.add_argument('file', type=FileStorage, location='files')
            args = self.parser.parse_args()
            post = PostModel(
                Title=args['title'],
                Author_id=args['user_id'],
                Content=args['content'],
                Type=0
            )
            db.session.add(post)
            db.session.commit()
            file.upload_resource_post(args['file'], post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Post(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, post_id):
        try:
            post = PostModel.query.get(post_id)
            identity = UserModel.query.get(post.Author_id)
            if post.file is not None:
                has_file = True
            else:
                has_file = False
            data = {
                'post_id': post.Post_id,
                'user': post.Author_id,
                'user_id': identity.nickname,
                'time': str(post.Date),
                'title': post.Title,
                'content': post.Content,
                'type': post.Type,
                'user_identity': identity.utype,
                'file': 'file/post/' + str(post_id),
                'has_file': has_file
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, post_id):
        try:
            post = PostModel.query.get(post_id)
            file.delete_resource_post(post)
            replies = ReplyModel.query.filter_by(Belong_Post_id=post_id).all()
            for reply in replies:
                file.delete_resource_reply(reply)
            db.session.delete(post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, post_id):
        try:
            post = PostModel.query.get(post_id)
            if post.Type == 0:
                post.Type = 1
            else:
                post.Type = 0
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Post_Report(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        try:
            reports = PostReportModel.query.all()
            data = []
            for report in reports:
                post = PostModel.query.get(report.post_id)
                data.append({
                    'id': report.report_id,
                    'reporter_id': report.reporter_id,
                    'content': report.content,
                    'author_id': post.Author_id,
                    'title': post.Title,
                    'post_content': post.Content,
                    'post_id': report.post_id
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self):
        try:
            self.parser.add_argument('post_id', type=int, location='args')
            self.parser.add_argument('reporter_id', type=str, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()
            report = PostReportModel(
                post_id=args['post_id'],
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
            report = PostReportModel.query.get(args['report_id'])
            db.session.delete(report)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

