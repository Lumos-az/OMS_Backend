from flask import render_template,request
from flask_mail import Message
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy import exc
from smtplib import SMTPDataError
from models import db
from common import code, pretty_result,gloVar
from models.user import UserModel
from common.auth import create_login_token, verify_login_token


class FindPassword(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.a = 0
    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('email', type=str, location="args")
        args = self.parser.parse_args()
        print(args)
        user = UserModel.query.get(args['uid'])
        
        try:
            if(user is None or user.emailAddr != args['email']):
                return pretty_result(code.OTHER_ERROR, data = '请输入正确的身份证号码和邮箱地址!')
            msg = Message(subject='test',recipients=[args['email']])
            msg.body = '您好，您的账户密码为'+user.password+'!'
            gloVar.get_value('mailData').send(msg)
            return pretty_result(code.OK)
        except SMTPDataError as e:
            print(e)
            return pretty_result(code.OTHER_ERROR)


        
        
       
        
        
    
    