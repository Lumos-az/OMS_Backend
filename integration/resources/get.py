from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.Hosiptal import HospitalModel
from models.Department import DepartmentModel
from models.DepartmentJoin import DepartmentJoinModel
from models.Doctor import DoctorModel
from models.BookingTime import BookingTimeModel
from models.Disease import DiseaseModel
from models.Record import RecordModel
from models.Patient import PatientModel
from models.PatientJoin import PatientsJoinModel
from common import code, pretty_result
from sqlalchemy import or_, and_, func


class GetHospitalInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('hid', type=int, location='args')
            args = self.parser.parse_args()

            department = []
            de = DepartmentJoinModel.query.filter(DepartmentJoinModel.hid == args['hid']) \
                .join(DepartmentModel, DepartmentModel.Did == DepartmentJoinModel.did).group_by(
                DepartmentModel.cataloge) \
                .with_entities(DepartmentModel.cataloge, func.group_concat(DepartmentModel.Did),
                               func.group_concat(DepartmentModel.name))
            print(de[1])
            for d in de:
                room = []
                ids = d[1].split(',')
                rnames = d[2].split(',')
                for i in range(0, len(ids)):
                    room.append({
                        'id': ids[i],
                        'rname': rnames[i]
                    })
                department.append({
                    'name': d[0],
                    'room': room
                })
                hospital = HospitalModel.query.filter(HospitalModel.hid == args['hid'])
            data.append({
                'name': hospital[0].name,
                'pname': hospital[0].pname,
                'website': hospital[0].website,
                'telephone': hospital[0].phone,
                'address': hospital[0].address,
                'qualification': hospital[0].qualification,
                'departments': department
            })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetDepartmentInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        try:
            data = []
            disease = []
            self.parser.add_argument('Did', type=int, location='args')
            args = self.parser.parse_args()
            diseases = DiseaseModel.query.filter(DiseaseModel.Did == args['Did'])
            for d in diseases:
                disease.append({
                    'iid': d.iid,
                    'iname': d.iname
                })
            departments = DepartmentModel.query.filter(DepartmentModel.Did == args['Did'])
            print(departments)
            data.append({
                'name': departments[0].name,
                'desp': departments[0].desp,
                'disease': disease
            })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetHospitalbyDepartment(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('Did', type=int, location='args')
            args = self.parser.parse_args()
            hospitals = DepartmentJoinModel.query.filter(DepartmentJoinModel.did == args['Did']) \
                .join(HospitalModel, HospitalModel.hid == DepartmentJoinModel.hid) \
                .with_entities(HospitalModel.hid, HospitalModel.name, HospitalModel.pname,
                               HospitalModel.website, HospitalModel.phone, HospitalModel.address).limit(5)
            print(hospitals)
            for hospital in hospitals:
                data.append({
                    'hid': hospital[0],
                    'name': hospital[1],
                    'pname': hospital[2],
                    'website': hospital[3],
                    'telephone': hospital[4],
                    'address': hospital[5],
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetDoctorlistinfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('Did', type=int, location='args')
            self.parser.add_argument('hid', type=int, location='args')
            args = self.parser.parse_args()

            Doctors = DoctorModel.query.filter(DoctorModel.Depid == args['Did'], DoctorModel.hid == args['hid']) \
                .join(HospitalModel, HospitalModel.hid == DoctorModel.hid) \
                .join(DepartmentModel, DepartmentModel.Did == DoctorModel.Depid) \
                .with_entities(DoctorModel.did, DoctorModel.name, DoctorModel.phone, DoctorModel.profession,
                               HospitalModel.pname, DoctorModel.mail, DepartmentModel.name, HospitalModel.address,
                               DoctorModel.avatarUrl)

            print(Doctors)
            for Doctor in Doctors:
                data.append({
                    'did': Doctor[0],
                    'name': Doctor[1],
                    'phone': Doctor[2],
                    'profession': Doctor[3],
                    'atHospital': Doctor[4],
                    'mail': Doctor[5],
                    'atDepartment': Doctor[6],
                    'address': Doctor[7],
                    'avatarUrl': Doctor[8]
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetDoctorInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            time = []
            self.parser.add_argument('did', type=int, location='args')
            args = self.parser.parse_args()

            times = BookingTimeModel.query.filter(BookingTimeModel.did == args['did'])
            for t in times:
                time.append({
                    'key': t.tid,
                    'Date': str(t.date),
                    'time': t.time,
                    'state': t.state,
                    'isFull': 'true' if t.isFull == 1 else 'false'
                })
            doctor = DoctorModel.query.filter(DoctorModel.did == args['did']) \
                .join(HospitalModel, HospitalModel.hid == DoctorModel.hid) \
                .join(DepartmentModel, DepartmentModel.Did == DoctorModel.Depid) \
                .with_entities(DoctorModel.name, DoctorModel.avatarUrl, DoctorModel.profession,
                               DoctorModel.phone, DoctorModel.mail, HospitalModel.address, DepartmentModel.name,
                               HospitalModel.pname, DoctorModel.introduction, DoctorModel.skilledField)

            data.append({
                'name': doctor[0][0],
                'avatarUrl': doctor[0][1],
                'profession': doctor[0][2],
                'phone': doctor[0][3],
                'mail': doctor[0][4],
                'address': doctor[0][5],
                'atDepartment': doctor[0][6],
                'atHospital': doctor[0][7],
                'introduction': doctor[0][8],
                'skilledArea': doctor[0][9],
                'time': time
            })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetDiseaseInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            self.parser.add_argument('iid', type=int, location='args')
            args = self.parser.parse_args()
            diseases = DiseaseModel.query.filter(DiseaseModel.iid == args['iid'])
            data = {
                'iname': diseases[0].iname,
                'desp': diseases[0].desp,
                'reason': diseases[0].reason,
                'symptom': diseases[0].symptom,
                'treatment': diseases[0].treatment,
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetBookingRecord(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('uid', location='args')
            args = self.parser.parse_args()
            # 如果要倒序输出，在字段名前面加一个‘-’即可  .order_by(RecordModel.rid)
            records = PatientsJoinModel.query.filter(PatientsJoinModel.uid == args['uid']) \
                .join(RecordModel, RecordModel.identityNumber == PatientsJoinModel.pid) \
                .join(HospitalModel, HospitalModel.hid == RecordModel.hospitalid) \
                .join(BookingTimeModel, RecordModel.timeid == BookingTimeModel.tid) \
                .join(DepartmentModel, RecordModel.departmentid == DepartmentModel.Did) \
                .join(DoctorModel, RecordModel.doctorid == DoctorModel.did) \
                .with_entities(RecordModel.rid, RecordModel.reservationNumber,
                               RecordModel.name, RecordModel.identityNumber, RecordModel.phoneNumber,
                               HospitalModel.pname, DepartmentModel.name, DoctorModel.name,
                               BookingTimeModel.date, BookingTimeModel.time, RecordModel.others) \
                .order_by(RecordModel.rid)

            print(records)
            for record in records:
                data.append({
                    'rid': record[0],
                    'reservationNumber': record[1],
                    'name': record[2],
                    'identifyNumber': record[3],
                    'phoneNumber': record[4],
                    'hospital': record[5],
                    'department': record[6],
                    'doctor': record[7],
                    'date': str(record[8]),
                    'time': record[9],
                    'others': record[10],
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class GetPatientInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('uid', location='args')
            args = self.parser.parse_args()
            defaultpatients = PatientsJoinModel.query.filter(PatientsJoinModel.uid == args['uid'],PatientsJoinModel.isDefault == 1)\
                .join(PatientModel,PatientModel.pid == PatientsJoinModel.pid).with_entities(PatientModel.pid,PatientModel.name,
                                                                                            PatientModel.age,PatientModel.sex,
                                                                                            PatientModel.phoneNumber,PatientModel.other,
                                                                                            PatientsJoinModel.isDefault)
            for defaultpatient in defaultpatients:
                data.append({
                    'Pid': defaultpatient.pid,
                    'name': defaultpatient.name,
                    'Age': defaultpatient.age,
                    'Sex': defaultpatient.sex,
                    'phoneNumber': defaultpatient.phoneNumber,
                    'other': defaultpatient.other,
                    'isDefault':defaultpatient.isDefault
                })

            patients = PatientsJoinModel.query.filter(PatientsJoinModel.uid == args['uid'],PatientsJoinModel.isDefault == 0)\
                .join(PatientModel,PatientModel.pid == PatientsJoinModel.pid).with_entities(PatientModel.pid,PatientModel.name,
                                                                                            PatientModel.age,PatientModel.sex,
                                                                                            PatientModel.phoneNumber,PatientModel.other,
                                                                                            PatientsJoinModel.isDefault)
            ##patients = PatientModel.query.filter(PatientsJoinModel.uid == args['uid']).join(PatientsJoinModel, PatientsJoinModel.pid == PatientModel.pid,PatientsJoinModel.isDefault == 0)
            for defaultpatient in patients:
                data.append({
                    'Pid': defaultpatient.pid,
                    'name': defaultpatient.name,
                    'Age': defaultpatient.age,
                    'Sex': defaultpatient.sex,
                    'phoneNumber': defaultpatient.phoneNumber,
                    'other': defaultpatient.other,
                    'isDefault':defaultpatient.isDefault
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class FreeTime(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            self.parser.add_argument('hid', location='args')
            self.parser.add_argument('depid', location='args')
            args = self.parser.parse_args()
            freeDoctor = DoctorModel.query.filter(DoctorModel.hid == args['hid'], DoctorModel.Depid == args['depid'])
            if freeDoctor.first() is None:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'Can not find the free doctor'
                return res
            time = DoctorModel.query.filter(DoctorModel.hid == args['hid'], DoctorModel.Depid == args['depid']) \
                .join(BookingTimeModel, BookingTimeModel.did == DoctorModel.did) \
                .with_entities(BookingTimeModel.date, BookingTimeModel.time, BookingTimeModel.state,
                               BookingTimeModel.isFull, DoctorModel.name, BookingTimeModel.tid, DoctorModel.did)
            print(time.first())
            for t in time:
                data.append({
                    'key': t[5],
                    'Date': str(t[0]),
                    'time': t[1],
                    'state': t[2],
                    'isFull': 'true' if t[3] == 1 else 'false',
                    'doctorName': t[4],
                    'doctorID': t[6]
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class get6doctor(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []

            Doctors = DoctorModel.query.filter(DoctorModel.did > 2, DoctorModel.did < 9) \
                .join(HospitalModel, HospitalModel.hid == DoctorModel.hid) \
                .join(DepartmentModel, DepartmentModel.Did == DoctorModel.Depid) \
                .with_entities(DoctorModel.did, DoctorModel.name, DoctorModel.phone, DoctorModel.profession,
                               HospitalModel.pname, DoctorModel.mail, DepartmentModel.name, HospitalModel.address,
                               DoctorModel.avatarUrl)

            print(Doctors)
            for Doctor in Doctors:
                data.append({
                    'did': Doctor[0],
                    'name': Doctor[1],
                    'phone': Doctor[2],
                    'profession': Doctor[3],
                    'atHospital': Doctor[4],
                    'mail': Doctor[5],
                    'atDepartment': Doctor[6],
                    'address': Doctor[7],
                    'avatarUrl': Doctor[8]
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class getAllHospital(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            Hospitals = HospitalModel.query.filter(HospitalModel.hid>0)
            print(Hospitals)
            for Hospital in Hospitals:
                data.append({
                    'name': Hospital.name,
                    'pname':Hospital.pname,
                    'hid': Hospital.hid,
                    'address': Hospital.address
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class getAllDoctor(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            Doctors = DoctorModel.query.filter(DoctorModel.did > 0) \
                .join(HospitalModel, HospitalModel.hid == DoctorModel.hid) \
                .join(DepartmentModel, DepartmentModel.Did == DoctorModel.Depid) \
                .with_entities(DoctorModel.did, DoctorModel.name, DepartmentModel.name, HospitalModel.name)
            print(Doctors)
            for Doctors in Doctors:
                data.append({
                    'name': Doctors[1],
                    'did':Doctors[0],
                    'atDe': Doctors[2],
                    'atHos': Doctors[3]
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class getAllDepartment(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        try:
            data = []
            Departments = DepartmentModel.query.filter(DepartmentModel.Did > 0)
            print(Departments)
            for Department in Departments:
                data.append({
                    'name': Department.name,
                    'Did':Department.Did,
                    'catalog': Department.cataloge,
                    'desp': str(Department.desp)
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
