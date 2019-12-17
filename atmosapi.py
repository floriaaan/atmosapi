#################################
#           SQL Part            #
#################################

import pymysql
import time
from datetime import datetime
from datetime import timedelta
import json
from flask_cors import CORS, cross_origin

atmosDB = pymysql.connect(
    host="127.0.0.1",
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

   

#################################
#           API Part            #
#################################


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app=app)
cors = CORS(app)


MEASURES = []



parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')



################# MEASURES CLASSES #################
# MeasureAll - print all measure of one probe
# GET
class MeasureAll(Resource):
    def get(self, probe_id):
        #SQL SELECT
        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s" %probe_id)
        ids=dbCursor.fetchall()
        MEASURES = []
        for i in range (1, len(ids) + 1):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
        return MEASURES

# Measure - print one measure
# GET & DELETE
class MeasureOne(Resource):
    def get(self, measure_id):
        mesure = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return mesure

    def delete(self, measure_id):
        dbCursor.execute("DELETE FROM 'MESURE' WHERE id_mesure= %d" % measure_id)
        
        return '', 204

# MeasureDay - print all measure of last day
# GET
class MeasureDay(Resource):
    def get(self, probe_id):
        DateNow = datetime.today()
        DateBefore = DateNow - timedelta(days=1)
        DateNow = DateNow.strftime("%Y-%m-%d %H:%M:%S")
        DateBefore = DateBefore.strftime("%Y-%m-%d %H:%M:%S")

        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s and mesure_date between '%s' and '%s'" %(probe_id, DateBefore, DateNow))
        ids=dbCursor.fetchall()
        MEASURES = []
        for i in range (1, len(ids)):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
        return MEASURES

# MeasureLast - print last measure of one probe
# GET
class MeasureLast(Resource):
    def get(self, probe_id):
        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_capteur = %s ORDER BY id_mesure DESC LIMIT 1" %probe_id)
        lastId = dbCursor.fetchone()
        lastId = int(lastId[0])
        mesure = {'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId), 'date': sql_select_date(lastId)}
        return mesure
        
# MeasurePost - inscribe in Database one measure 
# POST
class MeasurePost(Resource):
    def post(self, temp, humidity, probe_id):

        dateNow = datetime.today()
        dateNow = dateNow.strftime("%Y-%m-%d %H:%M:%S")

        values = {'temp': temp,'humidite': humidity, 'date': dateNow}

        
        dbCursor.execute("INSERT INTO MESURE (id_capteur, mesure_date, mesure_temp, mesure_humidite) VALUES (%s, '%s', %s, %s)" % (probe_id, dateNow, temp, humidity))
        atmosDB.commit()
        return values, 201

# MeasureDebug
# GET
class MeasureDebug(Resource):
    def get(self, measure_id):
        debug = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return debug


################## PROBES CLASSES ##################
# ProbeList - list all probes 
# GET
class ProbeList(Resource):
    def get(self):
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
        
        return PROBES, 200

# ProbePost - inscribe in Database one probe 
# POST
class ProbePost(Resource):
    def post(self, probe_name, latitude, longitude, measure_type):


        values = {'name': probe_name, 'latitude': latitude, 'longitude' : longitude}

        #CREATING PROBE
        dbCursor.execute("INSERT INTO SONDE (id_utilisateur, sonde_pos_latitude, sonde_pos_longitude, sonde_nom, sonde_active) VALUES (%s, %s, %s, '%s', 1)" % (1, latitude, longitude, probe_name))
        atmosDB.commit()

        dbCursor.execute("SELECT id_sonde FROM SONDE ORDER BY id_sonde DESC LIMIT 1")
        lastId = dbCursor.fetchone()
        lastId = int(lastId[0])
        #CREATING MEASURE TYPE OF PROBE
        dbCursor.execute("INSERT INTO CAPTEUR (id_sonde, capteur_mesure, capteur_valeur) VALUES (%d, %s, %d)" % (lastId, measure_type, 0))
        atmosDB.commit()
        return values, 201

# ProbeChangeState - update state of one probe 
# UPDATE
class ProbeChangeState(Resource):
    def update(self, probe_id):
        dbCursor.execute("SELECT sonde_active FROM SONDE WHERE id_sonde = %s" %probe_id)
        activity = dbCursor.fetchone()[0]

        if(activity == 1):
            dbCursor.execute("UPDATE SONDE SET sonde_active = 0 WHERE id_sonde = %s" %probe_id)
            atmosDB.commit()
        else: 
            if(activity == 0):
                dbCursor.execute("UPDATE SONDE SET sonde_active = 1 WHERE id_sonde = %s" %probe_id)
                atmosDB.commit()
        
        return 'Updated', 204

##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureAll, '/atmos/measure/<probe_id>')
api.add_resource(MeasureOne, '/atmos/measure/<measure_id>')
api.add_resource(MeasureDay, '/atmos/measure/day/<probe_id>')
api.add_resource(MeasureLast, '/atmos/measure/last/<probe_id>')
api.add_resource(MeasurePost, '/atmos/measure/add/<probe_id>/<temp>+<humidity>')

api.add_resource(MeasureDebug, '/atmos/debug/measure/<measure_id>')

api.add_resource(ProbeList, '/atmos/probe/')
api.add_resource(ProbePost, '/atmos/probe/add/<probe_name>+<latitude>+<longitude>+<measure_type>')
api.add_resource(ProbeChangeState, '/atmos/probe/state/change/<probe_id>')


if __name__ == '__main__':
    app.run(host="0.0.0.0")