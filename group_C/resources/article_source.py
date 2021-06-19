from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from common import code, pretty_result
from models.article_source import ArticleSourceModel


class ArticleSource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        try:
            sources = ArticleSourceModel.query.all()
            topnoticelist = []
            recommendread = {}
            hotarticle = []
            authoritypost = []
            allnotice = []
            for source in sources:
                if source.Type == 0:
                    topnoticelist.append({
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    })
                    allnotice.append({
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    })
                elif source.Type == 1:
                    recommendread = {
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    }
                elif source.Type == 2:
                    hotarticle.append({
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    })
                elif source.Type == 3:
                    authoritypost.append({
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    })
                elif source.Type == 4:
                    allnotice.append({
                        'id': source.Source_id,
                        'title': source.Title,
                        'author': source.Author,
                        'date': str(source.Date)[0:10]
                    })
            data = {
                'topNoticeList': topnoticelist,
                'recommendRead': recommendread,
                'hotArticle': hotarticle,
                'authorityPost': authoritypost,
                'allNotice': allnotice
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self):
        try:
            self.parser.add_argument('title', type=str, location='args')
            self.parser.add_argument('author', type=str, location='args')
            self.parser.add_argument('type', type=int, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()
            print(args)
            search = ArticleSourceModel.query.filter_by(Title=args['title']).first()
            if search is not None:
                return pretty_result(code.OTHER_ERROR)
            if args['type'] == 1:
                presource = ArticleSourceModel.query.filter_by(Type=args['type']).first()
                presource.Type = 2
                db.session.commit()
            source = ArticleSourceModel(
                Title=args['title'],
                Author=args['author'],
                Content=args['content'],
                Type=args['type']
            )
            db.session.add(source)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ArticleContent(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self, source_id):
        try:
            source = ArticleSourceModel.query.get(source_id)
            data = {
                'id': source.Source_id,
                'title': source.Title,
                'author': source.Author,
                'date': str(source.Date)[0:16],
                'content': source.Content,
                'type': source.Type
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)