from flask import Blueprint
from flask_restful import Api
from resources import post, reply, verify, article_source, file, email, get, patient, get_pres

routes = Blueprint('routes', __name__)

api = Api(routes)

api.add_resource(post.Posts, 'posts')
api.add_resource(post.Post, 'post/<int:post_id>')
api.add_resource(post.Post_Report, 'post_report')

api.add_resource(reply.Replies, 'replies/<int:post_id>')
api.add_resource(reply.Reply, 'reply/<int:reply_id>')
api.add_resource(reply.Reply_Report, 'reply_report')

api.add_resource(verify.Login, 'login')
api.add_resource(verify.IsLogin, 'islogin')
api.add_resource(verify.GetUsers, 'getUsers')
api.add_resource(verify.ChangeInfo, 'changeInfo')
api.add_resource(verify.ChangeRepoInfo, 'changeRepoInfo')
api.add_resource(verify.CanPost, 'CanPost')
api.add_resource(verify.CanReply, 'CanReply')
api.add_resource(verify.RegisterUser, 'registerPage')
api.add_resource(verify.ChangeCode, 'psdModPage')
api.add_resource(verify.CanRegisterDoctor, 'CanRegisterDoctor')
api.add_resource(verify.ReadUnactivatedDocs, 'DocIdeData')
api.add_resource(verify.ActivateDocs, 'DocIdeUpdate')
api.add_resource(verify.DocIdentify, 'DocIdentify')

api.add_resource(email.FindPassword, 'FindPasswordPage')

api.add_resource(article_source.ArticleSource, 'articleSource')
api.add_resource(article_source.ArticleContent, 'article/<int:source_id>')
api.add_resource(article_source.SourceList, 'articleList')
api.add_resource(article_source.SearchSource, 'articleList/search/<string:key>')

api.add_resource(file.PostFile, 'file/post/<int:id>')
api.add_resource(file.ReplyFile, 'file/reply/<int:id>')

api.add_resource(get.GetPatientInfo, 'getPatientInfo')
api.add_resource(get.GetBookingRecord, 'getBookingRecord')
api.add_resource(get.GetDiseaseInfo, 'getDiseaseInfo')
api.add_resource(get.GetDoctorInfo, 'getDoctorInfo')
api.add_resource(get.GetDoctorlistinfo, 'getDoctorlistinfo')
api.add_resource(get.GetHospitalbyDepartment, 'getHospitalbyDepartment')
api.add_resource(get.GetDepartmentInfo, 'getDepartmentInfo')
api.add_resource(get.GetHospitalInfo, 'getHospitalInfo')
api.add_resource(get.FreeTime, 'FreeTime')
api.add_resource(get.get6doctor, 'get6doctor')
api.add_resource(get.getAllHospital, 'getAllHospital')
api.add_resource(get.getAllDoctor, 'getAllDoctor')
api.add_resource(get.getAllDepartment, 'getAllDepartment')

api.add_resource(patient.UpdateBooking, 'updateBooking')
api.add_resource(patient.DeletePatient, 'deletePatient')
api.add_resource(patient.NewPatientInfo, 'newPatientInfo')
api.add_resource(patient.UpdatePatientInfo, 'updatePatientInfo')
api.add_resource(patient.newBooking, 'newBooking')
api.add_resource(patient.registerBydoctor, 'registerBydoctor')
api.add_resource(patient.registerByDepartment, 'registerByDepartment')
api.add_resource(patient.setDefaultPatient, 'setDefaultPatient')
api.add_resource(patient.NewUserPatientInfo, 'NewUserPatientInfo')

api.add_resource(get_pres.Prescriptions,'prescriptions')
api.add_resource(get_pres.Usage,'usage/<int:pres_id>')
api.add_resource(get_pres.Prescription,'prescription/<int:pres_id>')