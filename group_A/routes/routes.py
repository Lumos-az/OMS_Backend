from flask import Blueprint
from flask_restful import Api
from resources import post, reply, verify, article_source, get

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







api.add_resource(verify.CanRegisterDoctor, 'CanRegisterDoctor')

## 线上预约模块涉及的api

##get api===============================================================================================================

## http://127.0.0.1:5003/getPatientInfo?uid=330101199901010111
## 输入用户id获得该用户名下的就诊人信息
## 这里应该使用token和post比较合适，但是按照prd
api.add_resource(get.GetPatientInfo, 'getPatientInfo')

## http://127.0.0.1:5003/getBookingRecord?uid=330101199901010111
## 输入用户id获得该用户的挂号记录
## 这里应该使用token和post比较合适，但是按照prd
api.add_resource(get.GetBookingRecord, 'getBookingRecord')

## http://127.0.0.1:5003/getDiseaseInfo?iid=1
## 输入疾病id获得该疾病的信息
api.add_resource(get.GetDiseaseInfo, 'getDiseaseInfo')

## http://127.0.0.1:5003/getDoctorInfo?did=1
## 输入医生id获得该医生的信息
api.add_resource(get.GetDoctorInfo, 'getDoctorInfo')

## http://127.0.0.1:5003/getDoctorlistinfo?Did=1&hid=1
## 输入医院id和科室信息获得具有该科室的医生信息
api.add_resource(get.GetDoctorlistinfo, 'getDoctorlistinfo')

## http://127.0.0.1:5003/getHospitalbyDepartment?Did=2
## 输入科室id获得具有该科室的医院信息（最多5家）用于界面渲染
api.add_resource(get.GetHospitalbyDepartment, 'getHospitalbyDepartment')

## http://127.0.0.1:5003/getDepartmentInfo?Did=2
## 输入科室id获得科室相关信息用于界面渲染
api.add_resource(get.GetDepartmentInfo, 'getDepartmentInfo')

## http://127.0.0.1:5003/getHospitalInfo?hid=1
## 获得医院相关信息用于界面渲染
api.add_resource(get.GetHospitalInfo, 'getHospitalInfo')

## http://127.0.0.1:5003/FreeTime?hid=6&depid=5
## 查询医院某科室可以预约的医生排班
api.add_resource(get.FreeTime,'FreeTime')

## http://127.0.0.1:5003//get6doctor
##获取6个医生list
api.add_resource(get.get6doctor,'get6doctor')

##http://127.0.0.1:5003//getAllHospital
##获取所有医院list
api.add_resource(get.getAllHospital,'getAllHospital')

##http://127.0.0.1:5003//getAllDoctor
##获取所有医生list
api.add_resource(get.getAllDoctor,'getAllDoctor')

##http://127.0.0.1:5003//getAllDepartment
##获取所有的科室list
api.add_resource(get.getAllDepartment,'getAllDepartment')




## post api ============================================================================================================

## http://127.0.0.1:5003/updateBooking?rid=1003
## 修改待就诊的预约  方法选择post
## 注意 这里是‘待就诊’，不是‘未就诊’
api.add_resource(post.UpdateBooking, 'updateBooking')

## http://127.0.0.1:5003/deletePatient?pid=330100100101010101==>删除
## 删除就诊人信息
api.add_resource(post.DeletePatient, 'deletePatient')

## http://127.0.0.1:5003/newPatientInfo?uid=330101199901010111&pid=330100010101121110&name=小季&age=18&sex=男&phoneNumber=1234567879&other=吃吃喝喝
## 新增就诊人信息
api.add_resource(post.NewPatientInfo, 'newPatientInfo')

## http://127.0.0.1:5003/updatePatientInfo?pid=301000101011211103&age=17
## pid是必须的，否则会返回找不到就诊人，其他可以空着。同时，在这里没有更新PatientsJoin的视图
## 更新就诊人信息
## 方法用post 别用什么update
api.add_resource(post.UpdatePatientInfo, 'updatePatientInfo')

## http://127.0.0.1:5003/newBooking
##医生自己新增排版时间
api.add_resource(post.newBooking,'newBooking')

## http://127.0.0.1:5003/registerBydoctor?doctorid=6&timeid=22&pid=330100010101124444
## 按医生新增挂号，会判断是否冲突
api.add_resource(post.registerBydoctor, 'registerBydoctor')

## http://127.0.0.1:5003//registerByDepartment?hid=6&depid=4&date=2021-05-27&pid=330100010101124444&time=11:00-12:00
## 按科室新增挂号，会判断是否冲突
api.add_resource(post.registerByDepartment, 'registerByDepartment')

##http://127.0.0.1:5003//setDefaultPatient?uid=330101199901010111&pid=330302200001262427
##设置默认就诊人
api.add_resource(post.setDefaultPatient,'setDefaultPatient')

##http://127.0.0.1:5003//NewUserPatientInfo?uid=33012219970101291X
##新建用户时将该用户自动新建为就诊人并设置为默认
api.add_resource(post.NewUserPatientInfo,'NewUserPatientInfo')