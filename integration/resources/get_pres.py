from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.get_pres import PresModel
from common import code, pretty_result


class Prescriptions(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            prescriptions = PresModel.query.all()
            for pres in prescriptions:
                data.append({
                    'pres_id': pres.pres_id,
                    'user_id': pres.user_id,
                    'doctor_id': pres.doctor_id,
                    'information': pres.information,
                    'time': pres.time,
                    'prescription': pres.prescription
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self):
        try:
            self.parser.add_argument('pres_id', type=str, location='args')
            self.parser.add_argument('user_id', type=str, location='args')
            self.parser.add_argument('doctor_id', type=str, location='args')
            self.parser.add_argument('information', type=str, location='args')
            self.parser.add_argument('time', type=str, location='args')
            self.parser.add_argument('prescription', type=str, location='args')
            args = self.parser.parse_args()
            print(args)
            pres = PresModel(
                pres_id = args['pres_id'],
                user_id = args['user_id'],
                doctor_id = args['doctor_id'],
                information = args['information'],
                time = args['time'],
                prescription = args['prescription']
            )
            db.session.add(pres)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class Prescription(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self,pres_id):
        try:
            pdata = PresModel.query.get(pres_id)
            medinformation = pdata.prescription.split(';')
            test1 = []
            data = []
            for i in range(0,len(medinformation) - 1):
                test1 = medinformation[i].split(' ')
                test = {
                    'medNameZh': test1[0],
                    'medIcon': test1[1],
                    'mednumber': test1[2],
                    'medusage': test1[3]
                }

            data = {
                'pres_id': pdata.pres_id,
                'user_id': pdata.user_id,
                'doctor_id': pdata.doctor_id,
                'information': pdata.information,
                'time': pdata.time,
                'prescription': pdata.prescription,
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class Usage(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, pres_id):
        try:
            pdata = PresModel.query.get(pres_id)  # 这一步无法获取pdata
            medinformation = pdata.prescription.split(';')
            data = []
            for i in range(0, len(medinformation)):
                test1 = medinformation[i].split(' ')
                test = {
                    'medNameZh': test1[0],
                    'medIcon': test1[1],
                    'mednumber': test1[2],
                    'medusage': test1[3]
                }
                data.append(test)

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
