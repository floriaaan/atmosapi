#################################
#           SQL Part            #
#################################

import pymysql
import time
import json

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
    returndate = date#.strftime("%Y-%m-%d %H:%M:%S")
    return returndate

def sql_select_temp(id):
    #Temp of Measures
    dbCursor.execute("SELECT mesure_temp FROM MESURE WHERE id_mesure='%s'" % id)
    temp = json.dumps(dbCursor.fetchall())
    return temp

def sql_select_humid(id):
    #Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
    humid = json.dumps(dbCursor.fetchall())
    return humid

def getOne(id):
    str_mesure = {'temp': sql_select_temp(id), 'humidite': sql_select_humid(id), 'date': sql_select_date(id)}
    print(str_mesure)

def getList():
    dbCursor.execute("SELECT id_mesure FROM MESURE")
    ids=dbCursor.fetchall()
    MEASURES = []
    for i in range (1, len(ids)):
        MEASURES.append({'temp': sql_select_temp(i), 'humidite': sql_select_humid(i), 'date': sql_select_date(i)})
    print(MEASURES)

getList()
