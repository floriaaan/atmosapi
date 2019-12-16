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

# MeasureAll
# GET
class MeasureAll(Resource):
    def get(self):
        #SQL SELECT
        dbCursor.execute("SELECT id_mesure FROM MESURE")
        ids=dbCursor.fetchall()
        MEASURES = []
        for i in range (1, len(ids)):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
        return MEASURES

# Measure
# GET & DELETE & POST
class MeasureOne(Resource):
    def get(self, measure_id):
        mesure = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return mesure

    def delete(self, measure_id):
        dbCursor.execute("DELETE FROM 'MESURE' WHERE id_mesure='%d'" % measure_id)
        
        return '', 204

    

# MeasureList - which list all measure of last day
# GET
class MeasureList(Resource):
    def get(self):
        DateNow = datetime.today()
        DateBefore = DateNow - timedelta(days=1)
        DateNow = DateNow.strftime("%Y-%m-%d %H:%M:%S")
        DateBefore = DateBefore.strftime("%Y-%m-%d %H:%M:%S")

        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE mesure_date between '%s' and '%s'" %(DateBefore, DateNow))
        ids=dbCursor.fetchall()
        MEASURES = []
        for i in range (1, len(ids)):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]), 'date': sql_select_date(ids[i - 1])})
        return MEASURES

class MeasureLast(Resource):
    def get(self):
        dbCursor.execute("SELECT id_mesure FROM MESURE ORDER BY id_mesure DESC LIMIT 1")
        lastId = dbCursor.fetchone()
        lastId = int(lastId[0])
        mesure = {'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId), 'date': sql_select_date(lastId)}
        return mesure
        
# MeasurePost
# POST
class MeasurePost(Resource):
    def post(self, temp, humidity):

        dateNow = datetime.today()
        dateNow = dateNow.strftime("%Y-%m-%d %H:%M:%S")

        values = {'temp': temp,'humidite': humidity, 'date': dateNow}

        
        dbCursor.execute("INSERT INTO MESURE (id_capteur, mesure_date, mesure_temp, mesure_humidite) VALUES (%d, '%s', %s, %s)" % (1, dateNow, temp, humidity))
        atmosDB.commit()
        return values, 201

# MeasureDebug
# GET
class MeasureDebug(Resource):
    def get(self, measure_id):
        debug = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return debug




##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureAll, '/atmos/measure/')
api.add_resource(MeasureOne, '/atmos/measure/<measure_id>')
api.add_resource(MeasureList, '/atmos/measureList/')
api.add_resource(MeasureLast, '/atmos/measureLast/')
api.add_resource(MeasurePost, '/atmos/measureAdd/<temp>+<humidity>')


api.add_resource(MeasureDebug, '/atmos/debug/measure/<measure_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")