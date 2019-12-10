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

#Date of Measures
dbCursor.execute("SELECT mesure_date from MESURE")
measuresDate_SQL = dbCursor.fetchall();

#Temperature of Measures
dbCursor.execute("SELECT mesure_temp from MESURE")
measuresTemp_SQL = dbCursor.fetchall();

#Humidity of Measures
dbCursor.execute("SELECT mesure_humidite from MESURE")
measuresHumidite_SQL = dbCursor.fetchall();

#All of Measures
#dbCursor.execute("SELECT * from MESURE")
#measureTable_SQL = dbCursor.fetchall()



#################################
#           API Part            #
#################################


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app=app)

MEASURES = dict

for x in measureID_SQL:
    MEASURES[x] = {
        'x': {"'temp':" + measuresTemp_SQL[x] +" , 'humidite':" + measuresHumidite_SQL[x] +" , 'date':" + measuresDate_SQL[x]}
    }


# MEASURES = {
#     '1': {'temp': '20.5', 'humidite': '30%', 'date': '09/12/2019 17:30'},
#     '2': {'temp': '19.3', 'humidite': '50%', 'date': '09/12/2019 18:30'},
#     '3': {'temp': '10.4', 'humidite': '90%', 'date': '09/12/2019 19:30'},
# }


def abort_exist(measure_id):
    if measure_id not in measureID_SQL:
        abort(404, message="Measure {} doesn't exist".format(measure_id))

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
        return MEASURES[measure_id]

    def delete(self, measure_id):
        abort_exist(measure_id)
        del MEASURES[measure_id] # SQL DELETE
        return '', 204

    def post(self, measure_id):
        args = parser.parse_args()
        values = {'temp': args['temp'],'humidite': args['humidite'], 'date': args['date']}
        MEASURES[measure_id] = values
        #SQL INSERT
        return values, 201


# MeasureListAll
# GET
class MeasureListAll(Resource):
    def get(self):
        return MEASURES

# MeasureListFiveLast
# GET
class MeasureListFiveLast(Resource):
    def get(self):
        return MEASURES


##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureListAll, '/atmos/measureListAll/')
api.add_resource(MeasureListFiveLast, '/atmos/measureList/')
api.add_resource(Measure, '/atmos/measure/<measure_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")