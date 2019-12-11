#################################
#           SQL Part            #
#################################

import pymysql

atmosDB = pymysql.connect(
    host="127.0.0.1",
    user="atmos",
    passwd="atmos",
    charset="utf8",
    db="atmos"
)

dbCursor = atmosDB.cursor()


#Acquiring Datas from MariaDB server
#ID of Measures
dbCursor.execute("SELECT id_mesure FROM MESURE")
measureID_SQL = dbCursor.fetchall()

def sql_select_date(id):
    #Date of Measures
    dbCursor.execute("SELECT mesure_date FROM MESURE WHERE id_mesure='%d'" % id)
    date = dbCursor.fetchall();
    return date

def sql_select_temp(id):
    #Temp of Measures
    dbCursor.execute("SELECT mesure_temp FROM MESURE WHERE id_mesure='%d'" % id)
    temp = dbCursor.fetchall();
    return temp

def sql_select_humid(id):
    #Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%d'" % id)
    humid = dbCursor.fetchall();
    return humid

#################################
#           API Part            #
#################################


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app=app)

MEASURES = []


def abort_exist(measure_id):
    #if measure_id not in measureID_SQL:
        #abort(404, message="Measure {} doesn't exist".format(measure_id))
    print("debug purposes")

parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')


# Measure
# GET & DELETE & POST
class Measure(Resource):
    def get(self, measure_id):
        abort_exist(measure_id)
        #SQL SELECT
        str_mesure = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id), 'date': sql_select_date(measure_id)}
        return str_mesure

    def delete(self, measure_id):
        abort_exist(measure_id)
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


# MeasureListAll
# GET
class MeasureListAll(Resource):
    def get(self):
        debug = {'temp': sql_select_temp(1), 'humidite': sql_select_humid(1), 'date': sql_select_date(1)}
        return debug

# MeasureListFiveLast
# GET
class MeasureListFiveLast(Resource):
    def get(self):
        return MEASURES


##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureListAll, '/atmos/debug/')
api.add_resource(MeasureListFiveLast, '/atmos/measureList/')
api.add_resource(Measure, '/atmos/measure/<measure_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")