import pymysql
from random import *
db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com',user='root',passwd='Fuck2021',database='qtmdse')
cursor = db.cursor()

cursor.execute('select distinct medicineProducer from medicine')
da = cursor.fetchall()
for row in da:
    # print([row[0], ''.join([str(randint(0, 9)) for i in range(10)]))
     # '0.0', '0', '400' + ''.join([str(randint(0, 9)) for i in range(7)])])
    # continue
    cursor.execute('insert into producer(producerName, producerLicense, producerCredit, '
                   'producerCreditCount, producerContactInfo) values(%s,%s,%s,%s,%s)',
                   [row[0],''.join([str(randint(0,9)) for i in range(10)]),
                    '0.0','0','400'+''.join([str(randint(0,9)) for i in range(7)])])
db.commit()