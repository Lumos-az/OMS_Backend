import pymysql
import json
from pprint import pprint
from collections import defaultdict
from decimal import Decimal

'''
filter 格式：
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

如果不需要用到某几项筛选条件，请将第一个参数设为''（空字符串）

'''


def gen_filter(filters: dict):
    fa = []

    curk = 'medicineProducer'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == 'exact':
            qs = '''%s = '%s' ''' % (curk, curv[0])
        elif cond == 'exact not':
            qs = '''%s <> '%s' ''' % (curk, curv[0])
        elif cond == 'fuzzy':
            qs = '''%s like '%%%%%s%%%%' ''' % (curk, curv[0])
        elif cond == 'fuzzy not':
            qs = '''%s not like '%%%%%s%%%%' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    curk = 'medicineMainFunction'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == '':
            qs = '''%s like '%%%%%s%%%%' ''' % (curk, curv[0])
        elif cond == 'not':
            qs = '''%s not like '%%%%%s%%%%' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    curk = 'medicineSuitable'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == '':
            qs = '''%s like '%%%%%s%%%%' ''' % (curk, curv[0])
        elif cond == 'not':
            qs = '''%s not like '%%%%%s%%%%' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    curk = 'medicineTypeMajor'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == '':
            qs = '''%s = '%s' ''' % (curk, curv[0])
        elif cond == 'not':
            qs = '''%s <> '%s' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    curk = 'medicineTypeMinor'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == '':
            qs = '''%s = '%s' ''' % (curk, curv[0])
        elif cond == 'not':
            qs = '''%s <> '%s' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    curk = 'isOTC'
    curv = filters[curk]
    if len(curv[0]) > 0:
        cond = curv[1]
        if cond == '':
            qs = '''%s = '%s' ''' % (curk, curv[0])
        elif cond == 'not':
            qs = '''%s <> '%s' ''' % (curk, curv[0])
        else:
            raise Exception('Argument Error')
        fa.append(qs)

    return ' and '.join(fa)


def search_by_name_fuzzy(text, filters):  # 模糊匹配
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    ft = '%' + text + '%'
    filtstr = gen_filter(filters)
    if len(filtstr) > 0:
        cursor.execute('select * from medicine where (medicineNameZh like %s or medicineNameEn like %s'
                       ' or medicineNameAlias like %s) and (' + filtstr + ')', [ft, ft, ft])
    else:
        cursor.execute('select * from medicine where medicineNameZh like %s or medicineNameEn like %s'
                       ' or medicineNameAlias like %s', [ft, ft, ft])
    # cursor.execute('select * from medicine where (medicineNameZh like %s or medicineNameEn like %s'
    #                ' or medicineNameAlias like %s) and true', [ft, ft, ft])
    return cursor.fetchall()


def search_by_name_exact(text, filters):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from medicine where (medicineNameZh = %s or medicineNameEn = %s'
                   ' or medicineNameAlias = %s) and (' + gen_filter(filters) + ')', [text, text, text])
    return cursor.fetchall()


'''
处方json格式：
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


def make_prescription(presc_json: dict):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor()
    cursor.execute('insert into prescription(patientUserID, items, prescriptTime) values (%s,%s,now())',
                   [presc_json['patient'], json.dumps(presc_json['items'])])
    db.commit()
    return 200


def get_medicine_by_id(cursor, mid):
    cursor.execute('select * from medicine where medicineID=%s', [mid])
    qr1 = cursor.fetchall()
    if len(qr1) == 0:
        raise Exception('%s: No such medicineID' % mid)
    return qr1[0]


def get_supply_info_by_id(cursor, sid, mid):
    cursor.execute('select * from supplier where supplierID=%s and medicineID=%s', [sid, mid])
    qr1 = cursor.fetchall()
    if len(qr1) == 0:
        raise Exception('No such (supplierID, medicineID):(%s, %s)' % (sid, mid))
    return qr1[0]


def get_supplier_for_a_medicine(cursor, mid):
    # 先随便找个supplier
    cursor.execute('select * from supplier where medicineID=%s', [mid])
    qr1 = cursor.fetchall()
    if len(qr1) == 0:
        raise Exception('%s: No supplier supplies such medicineID' % mid)
    return qr1[0]


def fetch_a_cart(cursor, userid):
    cursor.execute('select * from cart where patientUserID = %s', [userid])
    qr = cursor.fetchall()
    if len(qr) == 0:
        return defaultdict(int)
    else:
        res = defaultdict(int)
        itms = eval(qr[0]['items'])
        res.update(itms)
        return res


def prescription_to_cart(prescid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # cursor.execute('select * from prescription', [prescid])
    cursor.execute('select * from prescription where prescriptionID = %s', [prescid])
    qr = cursor.fetchall()
    if len(qr) == 0:
        raise Exception('No such prescriptionID')
    else:
        its = json.loads(qr[0]['items'])
        if len(its) == 0:
            raise Exception('Null prescription: %s' % prescid)
        items = fetch_a_cart(cursor, qr[0]['patientUserID'])
        for k, v in its.items():
            sp = get_supplier_for_a_medicine(cursor, k)
            items[str((k, str(sp['supplierID'])))] += v

    cursor.execute('delete from cart where patientUserID=%s', qr[0]['patientUserID'])
    cursor.execute('insert into cart(patientUserID, items) values(%s,%s)',
                   [qr[0]['patientUserID'], json.dumps(items)])

    db.commit()

    return 200


def find_suppliers_for_medicine(mid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from supplier where medicineID = %s', [mid])
    return cursor.fetchall()


def find_medicines_a_supplier_supplies(sid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from supplier where supplierID = %s', [sid])
    return cursor.fetchall()


def query_medicineID(mid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return get_medicine_by_id(cursor, mid)


'''
    返回购物车信息
'''


def displaycart(userid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cart = fetch_a_cart(cursor, userid)
    res = {'userID': str(userid), 'items': []}
    tot = Decimal('0.00')
    for k, v in cart.items():
        med_sup = eval(k)
        med = get_medicine_by_id(cursor, med_sup[0])
        sup = get_supply_info_by_id(cursor, med_sup[1], med_sup[0])
        st = int(v) * sup['price']
        res['items'].append({'medicine': med, 'supplier': sup, 'amount': v,
                             'subtotal': st})
        tot += st
    res['total'] = tot

    return res


'''
    编辑购物车
    格式：{"('18', '1')": 2, "('56', '2')": 8, "('85', '3')": 4}
'''


def editcart(userid, newjson):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('delete from cart where patientUserID=%s', [userid])
    cursor.execute('insert into cart(patientUserID, items) values(%s, %s)', [userid, json.dumps(newjson)])
    db.commit()
    return 200


'''
    添加浏览记录
'''


def add_history(userid, medicineid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from patientInfo where userID=%s', [userid])
    qr0 = cursor.fetchall()
    if len(qr0) == 0:
        raise Exception('No such userID:%s' % str(userid))
    cursor.execute('select * from medicine where medicineID=%s', [medicineid])
    qr1 = cursor.fetchall()
    if len(qr1) == 0:
        raise Exception('No such medicineID:%s' % str(medicineid))
    cursor.execute('insert into viewHistory(userID, medicineID, viewTime) values(%s, %s, now())',
                   [userid, medicineid])
    db.commit()


'''
    返回浏览记录
'''


def display_history(userid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from viewHistory natural join medicine where userID=%s order by viewTime desc', [userid])
    qr0 = cursor.fetchall()
    return qr0


'''
    添加收藏夹
'''


def add_favor(userid, medicineid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from patientInfo where userID=%s', [userid])
    qr0 = cursor.fetchall()
    if len(qr0) == 0:
        raise Exception('No such userID:%s' % str(userid))
    cursor.execute('select * from medicine where medicineID=%s', [medicineid])
    qr1 = cursor.fetchall()
    if len(qr1) == 0:
        raise Exception('No such medicineID:%s' % str(medicineid))
    cursor.execute('insert into favor(userID, medicineID, favorTime) values(%s, %s, now())',
                   [userid, medicineid])
    db.commit()


'''
    返回收藏夹
'''


def display_favor(userid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from favor natural join medicine where userID=%s order by favorTime desc', [userid])
    qr0 = cursor.fetchall()
    return qr0


'''
    从收藏夹中删除
'''


def remove_favor(userid, medicineid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('delete from favor where userID=%s and medicineID=%s', [userid, medicineid])
    db.commit()
    return 200


'''
    添加到购物车
    items_to_add 是一个json，格式如下
    {
        "('18', '1')": 2, 
        "('56', '2')": 8, 
        "('85', '3')": 4
        # 键是(药品id, 供应商id)， 值是数量
    }
'''


def add_to_cart(userid, items_to_add):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    its = items_to_add
    items = fetch_a_cart(cursor, userid)
    for k, v in its.items():
        items[str(k)] += v

    cursor.execute('delete from cart where patientUserID=%s', userid)
    cursor.execute('insert into cart(patientUserID, items) values(%s,%s)',
                   [userid, json.dumps(items)])

    db.commit()

    return 200


'''
    提交订单
'''


def submit_order(userid, medicineid, supplierid, amount):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute('insert into `order`(userID, medicineID, supplierID, amount, totPrice) values(%s,%s,%s,%s,%s)',
                   [userid, medicineid, supplierid, amount,
                    get_supply_info_by_id(cursor, supplierid, medicineid)['price'] * Decimal(amount)])

    db.commit()

    return 200


'''
    返回订单
'''


def display_order(userid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute(
        'select * from `order` natural join medicine natural join supplier where userID=%s order by orderid desc',
        [userid])

    return cursor.fetchall()


'''
    评价订单
'''


def comment_order(orderid, commentStars, commentStr):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    cursor.execute('update `order` set commentStars = %s, commentStr = %s where orderID = %s',
                   [commentStars, commentStr, orderid])

    db.commit()

    return 200


'''
    提交支付信息
    orderList每一项都是一个orderID
'''


def submit_payment_info(orderList, platform):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    tot = Decimal(0.00)
    for orderid in orderList:
        cursor.execute('select * from `order` where orderID=%s', [orderid])
        orderinfos = cursor.fetchall()
        if len(orderinfos) == 0:
            raise Exception('Order does not exist: %s' % str(orderid))
        orderinfo = orderinfos[0]
        cursor.execute('update `order` set ispaid=true where orderID=%s',
                       [orderinfo['orderID']])
        tot += orderinfo['totPrice']

    cursor.execute('insert into payment(payTime, payAmount, platform, orderList) values(now(), %s, %s, %s)',
                   [tot, platform, orderList])

    db.commit()

    return 200


def get_med_image(mid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor()
    cursor.execute('select medicineImages from medicinePics where medicineID=%s', [mid])
    qr = cursor.fetchall()
    if len(qr) == 0:
        raise Exception('No such medicineID:%s' % str(mid))
    return qr[0][0]


def recom(n):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from medicine where isOTC<>\'否\' order by rand() limit %s;', [n])
    qr = cursor.fetchall()
    return qr


def add_to_prescription(puid, itemjson, did, txt):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        'insert into prescription(patientUserID, items, prescriptTime, doctorID, prescriptionText) values(%s,%s,now(),%s,%s)',
        [puid, itemjson, did, txt])
    db.commit()
    return 200


def display_presciption(puid):
    db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                         database='qtmdse')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from prescription where patientUserID=%s order by prescriptTime desc', [puid])
    return cursor.fetchall()


filt = {
    'medicineProducer': ['华润三九(北京)药业有限公司', 'exact'],
    # value array 的第一个参数是搜索字符串， 第二个参数有4种取值：
    # 'exact' 精确匹配
    # 'exact not' 排除精确匹配项
    # 'fuzzy' 模糊匹配
    # 'fuzzy not' 排除模糊匹配项

    'medicineMainFunction': ['急性智齿冠周炎', ''],
    # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
    # '' 模糊匹配
    # 'not' 排除模糊匹配项

    'medicineSuitable': ['对甲硝唑或吡咯类药物过敏患者禁用', ''],
    # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
    # '' 模糊匹配
    # 'not' 排除模糊匹配项

    'medicineTypeMajor': ['', ''],
    # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
    # '' 精确匹配
    # 'not' 排除精确匹配项

    'medicineTypeMinor': ['', ''],
    # value array 的第一个参数是搜索字符串， 第二个参数有2种取值：
    # '' 精确匹配
    # 'not' 排除精确匹配项

    'isOTC': ['', ''],
    # value array 的第一个参数是{'甲类OTC','乙类OTC','OTC','否'}中的一项， 第二个参数有2种取值：
    # '' 精确匹配
    # 'not' 排除精确匹配项
    # 其中'OTC'即甲类和乙类OTC的并集

}
# # print(search_by_name_exact('人工牛黄甲硝唑胶囊',filt))
# # print(make_prescription({
# #     'patient':2342, # 患者ID
# #     'items': {
# #         '18':1,
# #         '85':2,
# #         '56':4,
# #         # 键是药品id， 值是数量
# #     }
# # }))
# # pprint(submit_order(2342, 18, 1, 5))
# # pprint(submit_order(2342, 56, 2, 1))
# # pprint(submit_payment_info('[2,3]','Alipay'))
# # pprint(comment_order(2, 5, 'Fuck'))
# # pprint(comment_order(3, 5, 'Fuck-fuck'))
# # db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
# #                          database='qtmdse')
# # cursor = db.cursor(pymysql.cursors.DictCursor)
# # print(get_suppiler_for_a_medicine(cursor, '18'))
# # add_to_cart('2342', {
# #     ('18', '23'): 1,
# #     ('14', '23'): 2,
# #     ('23', '23'): 4,
# #     # 键是药品id， 值是数量
# # })
