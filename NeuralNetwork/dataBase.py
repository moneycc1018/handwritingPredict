import pymysql
import datetime as dt
import numpy as np
import configparser

config = configparser.ConfigParser(interpolation=None)
config.read("./config.ini")
db_user = config.get("db", "db_user")
db_password = config.get("db", "db_password")
db_database = config.get("db", "db_database")


#資料處理
def dataHandle(result_array):
    now_time = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    random_index = result_array[2]
    predict_num = str(np.int64(result_array[0]))
    true_num = str(result_array[1])
    predict_result = result_array[3]
    
    #查詢資料是否重複
    db = pymysql.connect(host='mysql-latest', port=3306, user=db_user, password=db_password, database=db_database, charset='utf8')
    cursor = db.cursor()
    query_sql = "select count(*) from handwriting_vae where random_index = %s" % (random_index)
    cursor.execute(query_sql)
    query_result = cursor.fetchone()[0]
    sql = ""
    if(query_result == 0):
        sql = createSql('insert', random_index, predict_num, true_num, predict_result, now_time)
    else:
        sql = createSql('update', random_index, predict_num, true_num, predict_result, now_time)
    cursor.execute(sql)
    db.commit()
    db.close()

    return ""

#組新增或更新sql
def createSql(flag, random_index, predict_num, true_num, predict_result, now_time):
    sql = ""
    if(flag == "insert"):
        sql = "insert into handwriting_vae (random_index, predict_num, \
               true_num, predict_result, create_time, update_time) \
               values (%s, '%s', '%s', %s, '%s', '%s')" % \
               (random_index, predict_num, true_num, predict_result, now_time, now_time)
    elif(flag == "update"):
        sql = "update handwriting_vae set predict_num='%s' ,predict_result=%s, \
               update_time='%s' where random_index=%s" % \
               (predict_num, predict_result, now_time, random_index)
    
    return sql