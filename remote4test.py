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
    temp = json.dumps(dbCursor.fetchone()[0])
    return temp

def sql_select_humid(id):
    #Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
    humid = json.dumps(dbCursor.fetchone()[0])
    return humid

def getOne(id):
    str_mesure = {'temp': sql_select_temp(id), 'humidite': sql_select_humid(id), 'date': sql_select_date(id)}
    print(str_mesure)

def getList(probe_id):
    DateNow = datetime.today()
    DateBefore = DateNow - timedelta(days=1)
    DateNow = DateNow.strftime("%Y-%m-%d %H:%M:%S")
    DateBefore = DateBefore.strftime("%Y-%m-%d %H:%M:%S")

    dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s and mesure_date between '%s' and '%s'" %(probe_id, DateBefore, DateNow))
    ids=dbCursor.fetchall()
    MEASURES = []
    for i in range (1, len(ids)):
        MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
    print(MEASURES)

def getLast(probe_id):
    dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s ORDER BY id_mesure DESC LIMIT 1" %probe_id)
    lastId = dbCursor.fetchone()
    lastId = int(lastId[0])
    mesure = {'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId), 'date': sql_select_date(lastId)}
    print(mesure)

def getAll(probe_id):
    dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s" %probe_id)
    ids=dbCursor.fetchall()
    MEASURES = []
    for i in range (1, len(ids) + 1):
        MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
    print(MEASURES)

def getAllProbes():
    dbCursor.execute("SELECT id_sonde FROM SONDE")
    ids=dbCursor.fetchall()
    PROBES = []
    for i in range (1, len(ids) + 1):
        dbCursor.execute("SELECT id_utilisateur FROM SONDE WHERE id_sonde='%s'" % i)
        user = json.dumps(dbCursor.fetchone()[0])

        dbCursor.execute("SELECT sonde_pos_latitude FROM SONDE WHERE id_sonde='%s'" % i)
        pos_x = json.dumps(dbCursor.fetchone()[0])

        dbCursor.execute("SELECT sonde_pos_longitude FROM SONDE WHERE id_sonde='%s'" % i)
        pos_y = json.dumps(dbCursor.fetchone()[0])

        dbCursor.execute("SELECT sonde_nom FROM SONDE WHERE id_sonde='%s'" % i)
        name = json.dumps(dbCursor.fetchone()[0])

        dbCursor.execute("SELECT sonde_active FROM SONDE WHERE id_sonde='%s'" % i)
        active = json.dumps(dbCursor.fetchone()[0])


        PROBES.append({'user': user, 'pos_x': pos_x, 'pos_y': pos_y, 'name': name, 'active': active})
    print(PROBES)

getAllProbes()
