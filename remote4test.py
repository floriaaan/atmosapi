#################################
#           SQL Part            #
#################################

import pymysql
import json
import time
from datetime import datetime
from datetime import timedelta

atmosDB = pymysql.connect(
    host="192.168.43.57",
    user="atmos",
    passwd="atmos",
    charset="utf8",
    db="atmos"
)

dbCursor = atmosDB.cursor()

def sql_select_date(id):
    #Date of Measures
    dbCursor.execute("SELECT mesure_date FROM MESURE WHERE id_mesure='%s'" % id)
    date = dbCursor.fetchall()
    returndate = date[0][0].strftime("%Y-%m-%d %H:%M:%S")
    return returndate

def sql_select_temp(id):
    #Temp of Measures
    dbCursor.execute("SELECT mesure_temp FROM MESURE WHERE id_mesure='%s'" % id)
    temp = json.dumps(dbCursor.fetchone())
    return temp

def sql_select_humid(id):
    #Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
    humid = json.dumps(dbCursor.fetchone())
    return humid

def getOne(id):
    str_mesure = {'temp': sql_select_temp(id), 'humidite': sql_select_humid(id), 'date': sql_select_date(id)}
    print(str_mesure)

def getList():
    DateNow = datetime.today()
    DateBefore = DateNow - timedelta(days=1)
    DateNow = DateNow.strftime("%Y-%m-%d")
    DateBefore = DateBefore.strftime("%Y-%m-%d")

    dbCursor.execute("SELECT id_mesure FROM MESURE WHERE mesure_date between '%s' and '%s'" %(DateBefore, DateNow))
    ids=dbCursor.fetchall()
    MEASURES = []
    for i in range (1, len(ids) + 1):
        MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
    print(MEASURES)

def getLast():
    dbCursor.execute("SELECT id_mesure FROM MESURE ORDER BY id_mesure DESC LIMIT 1")
    lastId = dbCursor.fetchone()
    lastId = int(lastId[0])
    mesure = {'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId), 'date': sql_select_date(lastId)}
    print(mesure)

getLast()
