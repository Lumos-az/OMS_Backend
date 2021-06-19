from drawpic import *
import pymysql

db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com', user='root', passwd='Fuck2021',
                     database='qtmdse')
cursor = db.cursor(pymysql.cursors.DictCursor)

cursor.execute('select * from medicine')
meds = cursor.fetchall()

for mi in meds:
    cursor.execute('update medicine set medicineImages=%s where medicineID=%s',[
        AddText().put_text(name_c=mi['medicineNameZh'], name_e=mi['medicineNameEn'], fac=mi['medicineProducer']),
        mi['medicineID']
    ])
    print(mi['medicineID'])
db.commit()
