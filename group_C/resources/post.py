from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.post import PostModel
from models.user import UserModel
from common import code, pretty_result


class Posts(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            posts = PostModel.query.all()
            for post in posts:
                data.append({
                    'post_id': post.Post_id,
                    'user_id': post.Author_id,
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
            args = self.parser.parse_args()
            print(args)
            post = PostModel(
                Title=args['title'],
                Author_id=args['user_id'],
                Content=args['content'],
                Type=0
            )
            db.session.add(post)
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
            data = {
                'post_id': post.Post_id,
                'user_id': post.Author_id,
                'time': str(post.Date),
                'title': post.Title,
                'content': post.Content,
                'type': post.Type,
                'user_identity': identity.identity
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, post_id):
        try:
            post = PostModel.query.get(post_id)
            db.session.delete(post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

