import pymysql

atmosDB = pymysql.connect(
    host="127.0.0.1",
    user="atmos",
    passwd="atmos",
    charset="utf8",
    db="atmos"
)

dbCursor = atmosDB.cursor()

dbCursor.execute("SELECT mesure_date from MESURE")
measuresDate = dbCursor.fetchall();

dbCursor.execute("SELECT mesure_temp from MESURE")
measuresTemp = dbCursor.fetchall();

dbCursor.execute("SELECT mesure_humidite from MESURE")
measuresHumidite = dbCursor.fetchall();

dbCursor.execute("SELECT * from MESURE")
measureTable = dbCursor.fetchall()

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app=app)

for x in measureTable:
    MEASURES[x] = {
        'x': {"'temp':" + measuresTemp[x] +" , 'humidite':" + measuresHumidite[x] +" , 'date':" + measuresDate[x]}
    }


# MEASURES = {
#     '1': {'temp': '20.5', 'humidite': '30%', 'date': '09/12/2019 17:30'},
#     '2': {'temp': '19.3', 'humidite': '50%', 'date': '09/12/2019 18:30'},
#     '3': {'temp': '10.4', 'humidite': '90%', 'date': '09/12/2019 19:30'},
# }


def abort_if_todo_doesnt_exist(measure_id):
    if measure_id not in MEASURES:
        abort(404, message="Measure {} doesn't exist".format(measure_id))

parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')


# Todo
# shows a single todo item and lets you delete a todo item
class Measure(Resource):
    def get(self, measure_id):
        abort_if_todo_doesnt_exist(measure_id)
        return MEASURES[measure_id]

    def delete(self, measure_id):
        abort_if_todo_doesnt_exist(measure_id)
        del MEASURES[measure_id]
        return '', 204

    def put(self, measure_id):
        args = parser.parse_args()
        values = {'temp': args['temp'],'humidite': args['humidite'], 'date': args['date']}
        MEASURES[measure_id] = values
        return values, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class MeasureList(Resource):
    def get(self):
        return MEASURES

    def post(self):
        args = parser.parse_args()
        measure_id = int(max(MEASURES.keys())) + 1
        measure_id = '%i' % measure_id
        MEASURES[measure_id] = {'temp': args['temp'], 'humidite': args['humidite'], 'date': args['date']}
        return MEASURES[measure_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(MeasureList, '/atmos/measures/')
api.add_resource(Measure, '/atmos/measure/<measure_id>')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")