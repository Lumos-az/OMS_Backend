from flask import Blueprint
from flask_restful import Api
from resources import post, reply, verify, article_source

routes = Blueprint('routes', __name__)

api = Api(routes)

api.add_resource(post.Posts, 'posts')
api.add_resource(post.Post, 'post/<int:post_id>')

api.add_resource(reply.Replies, 'replies/<int:post_id>')
api.add_resource(reply.Reply, 'reply/<int:reply_id>')

api.add_resource(verify.Login, 'login')
api.add_resource(verify.IsLogin, 'islogin')
api.add_resource(verify.GetUsers, 'getUsers')
api.add_resource(verify.ChangeInfo, 'changeInfo')
api.add_resource(verify.CanPost, 'CanPost')
api.add_resource(verify.CanReply, 'CanReply')

api.add_resource(article_source.ArticleSource, 'articleSource')
api.add_resource(article_source.ArticleContent, 'article/<int:source_id>')
api.add_resource(article_source.SourceList, 'articleList')
api.add_resource(article_source.SearchSource, 'articleList/search/<string:key>')

