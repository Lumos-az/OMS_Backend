from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.post import PostModel
from models.user import UserModel
from models.Record import RecordModel
from models.Patient import PatientModel
from models.BookingTime import BookingTimeModel
from models.Doctor import DoctorModel
from models.PatientJoin import PatientsJoinModel
from common import code, pretty_result
from sqlalchemy import or_, and_


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
            post = PostModel.query.get
            identity = UserModel.query.get
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
            post = PostModel.query.get
            db.session.delete(post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class NewPatientInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('pid', type=str, location="args")
        self.parser.add_argument('name', type=str, location="args")
        self.parser.add_argument('age', type=int, location="args")
        self.parser.add_argument('sex', type=str, location="args")
        self.parser.add_argument('phoneNumber', type=str, location="args")
        self.parser.add_argument('other', type=str, location="args")
        args = self.parser.parse_args()
        print(args)

        patient = PatientModel(
            pid=args['pid'],
            name=args['name'],
            age=args['age'],
            sex=args['sex'],
            phoneNumber=args['phoneNumber'],
            other=args['other'],
        )
        join = PatientsJoinModel(
            uid=args['uid'],
            pid=args['pid'],
            isDefault=int(0)
        )
        try:
            db.session.add(patient)
            db.session.commit()
            db.session.add(join)
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            res = pretty_result(code.DB_ERROR)
            res['Error'] = str(e)
            return res


class setDefaultPatient(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()
    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        self.parser.add_argument('pid', type=str, location="args")
        args = self.parser.parse_args()
        print(args)
        try:
            search = PatientsJoinModel.query.filter(PatientsJoinModel.uid == args['uid'], PatientsJoinModel.pid == args['pid'])
            if search.first() is None:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'Not find the person'
                return res
            else:
                db.session.query(PatientsJoinModel).filter(PatientsJoinModel.uid == args['uid'],PatientsJoinModel.isDefault == 1)\
                    .update({PatientsJoinModel.isDefault:int(0)}, synchronize_session=False)
                db.session.commit()
                db.session.query(PatientsJoinModel).filter(PatientsJoinModel.uid == args['uid'], PatientsJoinModel.pid == args['pid']) \
                    .update({PatientsJoinModel.isDefault:int(1)}, synchronize_session=False)
                db.session.commit()
                return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)



class UpdatePatientInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        try:
            self.parser.add_argument('pid', type=str, location="args")
            self.parser.add_argument('name', type=str, location="args")
            self.parser.add_argument('age', type=int, location="args")
            self.parser.add_argument('sex', type=str, location="args")
            self.parser.add_argument('phoneNumber', type=str, location="args")
            self.parser.add_argument('other', type=str, location="args")
            args = self.parser.parse_args()

            person = PatientModel.query.filter_by(pid=args['pid']).first()
            if person is None:
                res = pretty_result(code.PARAM_ERROR)
                res['Error'] = 'Not found the patient'
                return res
            if args['name'] is None:
                args['name'] = person.name
            if args['age'] is None:
                args['age'] = person.age
            if args['sex'] is None:
                args['sex'] = person.sex
            if args['phoneNumber'] is None:
                args['phoneNumber'] = person.phoneNumber
            if args['other'] is None:
                args['other'] = person.other
            patient = PatientModel.query.filter_by(pid=args['pid']).update(
                {'name': args['name'], 'age': args['age'], 'sex': args['sex'], 'phoneNumber': args['phoneNumber'],
                 'other': args['other']})
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            res = pretty_result(code.DB_ERROR)
            res['Error'] = str(e)
            return res


class DeletePatient(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        try:
            self.parser.add_argument('pid', location="args")
            args = self.parser.parse_args()
            search = PatientModel.query.filter(PatientModel.pid == args['pid'])
            if search.first() is None:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'Not find the person'
                return res
            else:
                db.session.query(PatientModel).filter(PatientModel.pid == args['pid']).delete()
                db.session.commit()
                return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class UpdateBooking(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        try:
            self.parser.add_argument('rid', location="args")
            args = self.parser.parse_args()
            search = RecordModel.query.filter(RecordModel.others == '待就诊', RecordModel.rid == args['rid'])
            tmp = search.first()
            print(search)
            if search.first() is None:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'Not found'
                return res
            else:
                db.session.query(RecordModel).filter(RecordModel.others == '待就诊', RecordModel.rid == args['rid']) \
                    .update({RecordModel.others: '已取消'}, synchronize_session=False)
                db.session.commit()
                db.session.query(BookingTimeModel).filter(BookingTimeModel.tid == tmp.timeid)\
                    .update({BookingTimeModel.isFull:int(0),BookingTimeModel.state:(tmp.reservationNumber-1)}, synchronize_session=False)
                db.session.commit()
                return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class newBooking(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()
    def post(self):
        try:
            self.parser.add_argument('did', type=int, location="args")
            self.parser.add_argument('Date', type=str, location="args")
            self.parser.add_argument('time', type=str, location="args")
            args = self.parser.parse_args()
            #print(args)
            booking = BookingTimeModel.query.filter(BookingTimeModel.did==args['did'],BookingTimeModel.date==args['Date'],BookingTimeModel.time==args['time'])
            if booking.first() is None:
                bookingtime = BookingTimeModel(
                    date=args['Date'],
                    time=args['time'],
                    isFull=0,
                    state=0,
                    did=args['did']
                )

                db.session.add(bookingtime)
                db.session.commit()
                return pretty_result(code.OK)
            else:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'Already has booking'
                return res

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            res = pretty_result(code.DB_ERROR)
            res['Error'] = str(e)
            return res


class registerBydoctor(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        try:
            self.parser.add_argument('doctorid', type=int, location="args")
            self.parser.add_argument('timeid', type=int, location="args")
            self.parser.add_argument('pid', type=int, location="args")
            args = self.parser.parse_args()
            # print(args)

            ##判断是否重复,先查出科室当日排班的tid，再差用待就诊的tid，两个join判断是否冲突
            HSrecord = DoctorModel.query.filter(DoctorModel.did == args['doctorid']).with_entities(DoctorModel.hid,DoctorModel.Depid).first()
            Date = BookingTimeModel.query.filter(BookingTimeModel.tid == args['timeid']).first()
            findresult = BookingTimeModel.query.join(RecordModel, RecordModel.timeid == BookingTimeModel.tid) \
                .filter(BookingTimeModel.date == Date.date, RecordModel.departmentid == HSrecord.Depid,
                        RecordModel.hospitalid == HSrecord.hid, \
                        RecordModel.identityNumber == args['pid'], RecordModel.others == '待就诊')

            if findresult.first() is None:
                ##更新state数据
                data = []
                time = BookingTimeModel.query.filter(BookingTimeModel.tid == args['timeid']).with_entities(
                    BookingTimeModel.tid, BookingTimeModel.did, BookingTimeModel.state, BookingTimeModel.date,
                    BookingTimeModel.time)
                tmp = time.first()
                if (time.first())[2] == 4:
                    res = pretty_result(code.DB_ERROR)
                    res['Error'] = 'Full'
                    return res
                elif (time.first())[2] == 3:
                    db.session.query(BookingTimeModel).filter(BookingTimeModel.tid == (time.first())[0]) \
                        .update({BookingTimeModel.isFull: int(1), BookingTimeModel.state: int(4)},
                                synchronize_session=False)
                    db.session.commit()
                else:
                    db.session.query(BookingTimeModel).filter(BookingTimeModel.tid == (time.first())[0]) \
                        .update({BookingTimeModel.state: int((time.first())[2] + 1)}, synchronize_session=False)
                    db.session.commit()

                ##存入新的挂号信息
                patient = PatientModel.query.filter(PatientModel.pid == args['pid']).first()
                doctor = DoctorModel.query.filter(DoctorModel.did == args['doctorid']).first()
                recode = RecordModel(
                    name=patient.name,
                    reservationNumber=int(tmp[2] + 1),
                    identityNumber=args['pid'],
                    phoneNumber=patient.phoneNumber,
                    hospitalid=doctor.hid,
                    timeid=args['timeid'],
                    doctorid=args['doctorid'],
                    departmentid=doctor.Depid,
                    others='待就诊'
                )
                db.session.add(recode)
                db.session.commit()

                ##输出更新后的time信息
                nows = BookingTimeModel.query.filter(BookingTimeModel.did == args['doctorid'])
                for now in nows:
                    data.append({
                        'key': now.tid,
                        'year': str(now.date)[0:4] + '年',
                        'day': str(now.date)[6:7] + '月' + str(now.date)[8:] + '日',
                        'Date': str(now.date),
                        'time': now.time,
                        'state': int(now.state),
                        'isFull': 'true' if now.state == 4 else 'false'
                    })
                return pretty_result(code.OK, data=data)
            else:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'already had record'
                return res


        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class registerByDepartment(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        try:
            data = []
            self.parser.add_argument('hid', location="args")
            self.parser.add_argument('depid', location="args")
            self.parser.add_argument('date', location="args")
            self.parser.add_argument('pid', location="args")
            self.parser.add_argument('time', location="args")
            args = self.parser.parse_args()

            findresult = BookingTimeModel.query.join(RecordModel, RecordModel.timeid == BookingTimeModel.tid) \
                .filter(BookingTimeModel.date == args['date'], RecordModel.departmentid == args['depid'],
                        RecordModel.hospitalid == args['hid'], \
                        RecordModel.identityNumber == args['pid'], RecordModel.others == '待就诊')

            if findresult.first() is None:
                # 根据时间，医院，部门获取医生的信息，返回book的编号，医生的id和医生的名字
                doctor = BookingTimeModel.query.join(DoctorModel, DoctorModel.did == BookingTimeModel.did) \
                    .filter(BookingTimeModel.time == args['time'], BookingTimeModel.date == args['date'],
                            DoctorModel.hid == args['hid'], DoctorModel.Depid == args['depid'],
                            BookingTimeModel.isFull == int(0)) \
                    .with_entities(BookingTimeModel.tid, DoctorModel.did, DoctorModel.name, BookingTimeModel.state)
                if doctor.first() is None:
                    res = pretty_result(code.DB_ERROR)
                    res['Error'] = 'Can not find the free doctor'
                    return res

                search = BookingTimeModel.query.filter(BookingTimeModel.tid == (doctor.first())[0])

                # 如果state+1到4了，修改isFull为0
                #
                tmp = doctor.first()

                if (doctor.first())[3] == 3:
                    db.session.query(BookingTimeModel).filter(BookingTimeModel.tid == (doctor.first())[0]) \
                        .update({BookingTimeModel.isFull: int(1), BookingTimeModel.state: int(4)},
                                synchronize_session=False)
                    db.session.commit()
                else:
                    db.session.query(BookingTimeModel).filter(BookingTimeModel.tid == (doctor.first())[0]) \
                        .update({BookingTimeModel.state: int((doctor.first())[3] + 1)}, synchronize_session=False)
                    db.session.commit()

                # 在record里面添加信息
                patient = PatientModel.query.filter(PatientModel.pid == args['pid']).first()
                recode = RecordModel(
                    name=patient.name,
                    reservationNumber=int(tmp[3] + 1),
                    identityNumber=args['pid'],
                    phoneNumber=patient.phoneNumber,
                    hospitalid=args['hid'],
                    timeid=tmp[0],
                    doctorid=tmp[1],
                    departmentid=args['depid'],
                    others='待就诊'
                )
                db.session.add(recode)
                db.session.commit()

                ##更新后的time
                freeDoctor = DoctorModel.query.filter(DoctorModel.hid == args['hid'],
                                                      DoctorModel.Depid == args['depid'])
                time = DoctorModel.query.filter(DoctorModel.hid == args['hid'], DoctorModel.Depid == args['depid']) \
                    .join(BookingTimeModel, BookingTimeModel.did == DoctorModel.did) \
                    .with_entities(BookingTimeModel.date, BookingTimeModel.time, BookingTimeModel.state,
                                   BookingTimeModel.isFull, DoctorModel.name)
                print(time.first())
                times = []
                for t in time:
                    times.append({
                        'Date': str(t[0]),
                        'time': t[1],
                        'state': t[2],
                        'isFull': 'true' if t[3] == 1 else 'false',
                        'doctorName': t[4]
                    })
                data.append({
                    'doctorName': tmp[2],
                    'times': times
                })

                return pretty_result(code.OK, data=data)
            else:
                res = pretty_result(code.DB_ERROR)
                res['Error'] = 'already had record'
                return res
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class NewUserPatientInfo(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        self.parser.add_argument('uid', type=str, location="args")
        args = self.parser.parse_args()
        print(args)

        defaultpatient=UserModel.query.filter(UserModel.uid==args['uid']).first()

        patient = PatientModel(
            pid=defaultpatient.uid,
            name=defaultpatient.name,
            age=defaultpatient.age,
            sex=defaultpatient.sex,
            phoneNumber=defaultpatient.phoneNumber,
            other=defaultpatient.other,
        )
        join = PatientsJoinModel(
            uid=args['uid'],
            pid=args['uid'],
            isDefault=int(1)
        )
        try:
            db.session.add(patient)
            db.session.commit()
            db.session.add(join)
            db.session.commit()
            return pretty_result(code.OK)

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            res = pretty_result(code.DB_ERROR)
            res['Error'] = str(e)
            return res