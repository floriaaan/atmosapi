#################################
#           SQL Part            #
#################################

import pymysql
import time
import json

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
    temp = json.dumps(dbCursor.fetchall())
    return temp

def sql_select_humid(id):
    #Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
    humid = json.dumps(dbCursor.fetchall())
    return humid

#################################
#           API Part            #
#################################


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app=app)

MEASURES = []



parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')


# Measure
# GET & DELETE & POST
class Measure(Resource):
    def get(self, measure_id):
        #SQL SELECT
        str_mesure = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return str_mesure

    def delete(self, measure_id):
        dbCursor.execute("DELETE FROM 'MESURE' WHERE id_mesure='%d'" % measure_id)
        # del MEASURES[measure_id] # SQL DELETE
        return '', 204

    def post(self, measure_id):
        args = parser.parse_args()
        values = {'temp': args['temp'],'humidite': args['humidite'], 'date': args['date']}
        # MEASURES[measure_id] = values
        #SQL INSERT
        dbCursor.execute("INSERT INTO MESURE (id_capteur, mesure_date, mesure_temp, mesure_humidite) VALUES (%d, '2019/12/09 17:30:00', %d, %d)" % (measure_id, args['temp'], args['humidite']))
        return values, 201


# MeasureDebug
# GET
class MeasureDebug(Resource):
    def get(self, measure_id):
        debug = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return debug

# MeasureList - which list five last measures
# GET
class MeasureList(Resource):
    def get(self):
        return MEASURES


##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureDebug, '/atmos/debug/measure/<measure_id>')
api.add_resource(MeasureList, '/atmos/measureList/')
api.add_resource(Measure, '/atmos/measure/<measure_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")