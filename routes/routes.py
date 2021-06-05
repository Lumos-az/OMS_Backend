from flask import Blueprint
from flask_restful import Api
from resources import verify,email

routes = Blueprint('routes', __name__)

api = Api(routes)


api.add_resource(verify.Login, 'login')
api.add_resource(verify.IsLogin, 'islogin')
api.add_resource(verify.GetUsers, 'getUsers')
api.add_resource(verify.ChangeInfo, 'changeInfo')
api.add_resource(verify.RegisterUser,'registerPage')
api.add_resource(verify.ChangeCode, 'psdModPage')
api.add_resource(verify.ReadUnactivatedDocs, 'DocIdeData')
api.add_resource(verify.ActivateDocs, 'DocIdeUpdate')
api.add_resource(verify.DocIdentify, 'DocIdentify')

api.add_resource(email.FindPassword,'FindPasswordPage')

