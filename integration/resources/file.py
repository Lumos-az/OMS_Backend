from flask import send_file
from flask_restful import Resource
from models.post import PostModel
from models.reply import ReplyModel


class PostFile(Resource):
    def get(self, id):
        resource = PostModel.query.get(id)
        return send_file('file/post/' + str(id) + '.' + resource.file, as_attachment=True)


class ReplyFile(Resource):
    def get(self, id):
        resource = ReplyModel.query.get(id)
        return send_file('file/reply/' + str(id) + '.' + resource.file, as_attachment=True)
