import pandas as pd
import pymysql

df = pd.read_excel('丁香园2.xlsx')

db = pymysql.connect(host='rm-bp1it523lbu3zr299jo.mysql.rds.aliyuncs.com',user='root',passwd='Fuck2021',database='qtmdse')
cursor = db.cursor()

for i in df.itertuples():
    l=[str(k) for k in list(i)]
    print(i)
    print(cursor.execute('insert into medicine values \
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        [l[0],l[4],l[5],l[6],l[7],l[3],
         l[8],l[10]+';'+l[15],l[1],l[2],None,None,
         l[11],l[13],l[12]
         ]))

db.commit()
