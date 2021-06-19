from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from routes import routes
import json
import simplejson
import datetime
from functools import partial

import api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app, supports_credentials=True)
app.register_blueprint(routes, url_prefix='/')


@app.route('/')
def hello_world():
    return 'Hello World231!'


class MyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return simplejson.JSONEncoder.default(self, obj)


# myjsonify = partial(simplejson.dumps, cls=MyEncoder)
def myjsonify(obj):
    return simplejson.dumps(obj, cls=MyEncoder).replace('nan', '')


def myjsonify_raw(obj):
    return simplejson.dumps(obj, cls=MyEncoder)


'''
filters 格式：


'''

'''
    请求格式：
    {
        "text":"甲硝唑",
        "filters:
        {
            'medicineProducer': ['华润三九(北京)药业有限公司','exact'],
            # value array 的第一个参数是搜索字符串， 第二个参数有4种取值：
                'exact' 精确匹配 
                'exact not' 排除精确匹配项 
                'fuzzy' 模糊匹配
                'fuzzy not' 排除模糊匹配项
        
            'medicineMainFunction': ['急性智齿冠周炎',''],
            # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
                '' 模糊匹配
                'not' 排除模糊匹配项
        
            'medicineSuitable': ['对甲硝唑或吡咯类药物过敏患者禁用',''],
            # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
                '' 模糊匹配
                'not' 排除模糊匹配项    
        
            'medicineTypeMajor': ['消化系统及代谢药',''],
            # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
                '' 精确匹配
                'not' 排除精确匹配项
        
            'medicineTypeMinor': ['口腔科用药',''],
            # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
                '' 精确匹配
                'not' 排除精确匹配项
        
            'isOTC':['甲类OTC',''],
            # value array 的第一个参数是{'甲类OTC','乙类OTC','OTC','否'}中的一项， 第二个参数有2种取值：
                '' 精确匹配
                'not' 排除精确匹配项
                其中'OTC'即甲类和乙类OTC的并集
        }

}

如果不需要用到某几项筛选条件，请将第一个参数设为''（空字符串）
'''


@app.route('/api/search-by-name-fuzzy', methods=['POST'])
def search_by_name_fuzzy():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.search_by_name_fuzzy(data['text'], data['filters']))


@app.route('/api/search-by-name-exact', methods=['POST'])
def search_by_namvae_exact():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.search_by_name_exact(data['text'], data['filters']))


'''
请求json格式：
{
    'patient':2342, # 患者ID
    'items': {
        '18':1,
        '85':2,
        '56':4,
        # 键是药品id， 值是数量
    }
}
'''


@app.route('/api/make-prescription', methods=['POST'])
def make_prescription():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.make_prescription(data))


'''
请求格式:
{
    "prescriptionID": 1
}

'''


@app.route('/api/prescription-to-cart', methods=['POST'])
def prescription_to_cart():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.make_prescription(data["prescriptionID"]))


'''
获取购物车内容
请求格式:
{
    "userID": 1
}

'''


@app.route('/api/displaycart', methods=['POST'])
def displaycart():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.displaycart(data["userID"]))


'''
覆盖购物车内容
请求格式:
{
    "userID": 1,
    "cart":{"('18', '1')": 2, "('56', '2')": 8, "('85', '3')": 4}
}

'''


@app.route('/api/editcart', methods=['POST'])
def editcart():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.editcart(data["userID"], data["cart"]))


'''
    添加浏览记录
    请求格式:
    {
        "userID":1,
        "medicineID":18
    }
'''


@app.route('/api/add-history', methods=['POST'])
def add_history():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.add_history(data["userID"], data["medicineID"]))


'''
    返回浏览记录
    请求格式:
    {
        "userID":1
    }
'''


@app.route('/api/display-history', methods=['POST'])
def display_history():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.display_history(data["userID"]))


'''
    添加收藏夹
    请求格式:
    {
        "userID":1,
        "medicineID":18
    }
'''


@app.route('/api/add-favor', methods=['POST'])
def add_favor():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.add_favor(data["userID"], data["medicineID"]))


'''
    返回收藏夹
    请求格式:
    {
        "userID":1
    }
'''


@app.route('/api/display-favor', methods=['POST'])
def display_favor():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.display_favor(data["userID"]))


'''
    从收藏夹中删除
    请求格式:
    {
        "userID":1,
        "medicineID":18
    }
'''


@app.route('/api/remove-favor', methods=['POST'])
def remove_favor():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.remove_favor(data["userID"], data["medicineID"]))


'''
    添加到购物车
    请求格式：
    {
        "userID": 1,
        "items":
        {
            "('18', '1')": 2, 
            "('56', '2')": 8, 
            "('85', '3')": 4
            # 键是(药品id, 供应商id)， 值是数量
        }
'''


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.add_to_cart(data["userID"], data["items"]))


'''
    提交订单
    请求格式：
    {
        "userID": 1,
        "medicineID": 18,
        "supplierID": 1,
        "amount": 1
    }
'''


@app.route('/api/submit-order', methods=['POST'])
def submit_order():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.submit_order(data["userID"], data["medicineID"], data["supplierID"], data["amount"]))


'''
    返回订单
    请求格式：
    {
        "userID": 1
    }
'''


@app.route('/api/display-order', methods=['POST'])
def display_order():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.display_order(data["userID"]))


'''
    评价订单
    请求格式：
    {
        "orderID": 1,
        "commentStars": 5,
        "commentStr": "Fuck"
    }
'''


@app.route('/api/comment-order', methods=['POST'])
def comment_order():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.comment_order(data["orderID"], data["ommentStars"], data["commentStr"]))


'''
    提交支付信息
    请求格式：
    {
        "orderList": [1,2,3], // 每一项都是一个orderID
        "platform": "Alipay"
    }
'''


@app.route('/api/submit-payment-info', methods=['POST'])
def submit_payment_info():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.submit_payment_info(data["orderList"], data["platform"]))


'''
    查询某一药品的供应商
    请求格式：
    {
        "medicineID":18
    }
'''


@app.route('/api/find-suppliers-for-medicine', methods=['POST'])
def find_suppliers_for_medicine():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.find_suppliers_for_medicine(data["medicineID"]))


'''
    查询某一药品
    请求格式：
    {
        "medicineID":18
    }
'''


@app.route('/api/query-medicineID', methods=['POST'])
def query_medicine():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.query_medicineID(data["medicineID"]))


'''
    请求某一药品的图片
    请求格式：
    {
        "medicineID":18
    }
'''


@app.route('/api/medicine-images', methods=['POST'])
def medicine_images():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify_raw(api.get_med_image(data["medicineID"]))


'''
    首页推荐
    n是需要返回的药品数目
    请求格式：
    {
        "n":10
    }
'''


@app.route('/api/recom', methods=['POST'])
def recom():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.recom(data["n"]))


'''
    添加处方
    请求格式：
    {
        "patientUserID":2342,
        "itemjson":"{\\"18\": 1, \\"56\": 4, \\"85\\": 2}",
        "doctorID":12,
        "text":"五十天内不能吃饭"
    }
'''


@app.route('/api/add-to-prescription', methods=['POST'])
def add_to_prescription():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.add_to_prescription(data["patientUserID"], data["itemjson"], data["doctorID"], data["text"]))


'''
获取某名患者的所有处方
请求格式:
{
    "userID": 1
}

'''


@app.route('/api/display-prescription', methods=['POST'])
def display_prescription():
    data = json.loads(request.get_data(as_text=True))
    return myjsonify(api.display_presciption(data["userID"]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
