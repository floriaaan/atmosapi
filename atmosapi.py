#################################
#           SQL Part            #
#################################

import pymysql
from datetime import datetime
from datetime import timedelta
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
    # Date of Measures
    dbCursor.execute("SELECT mesure_date FROM MESURE WHERE id_mesure='%s'" % id)
    date = dbCursor.fetchall()
    returndate = date[0][0].strftime("%Y-%m-%d %H:%M:%S")
    return returndate

def sql_select_temp(id):
    # Temp of Measures
    dbCursor.execute("SELECT mesure_temp FROM MESURE WHERE id_mesure='%s'" % id)
    temp = json.dumps(dbCursor.fetchone()[0])
    return temp

def sql_select_humid(id):
    # Humid of Measures
    dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
    humid = json.dumps(dbCursor.fetchone()[0])
    return humid


#################################
#           API Part            #
#################################


from flask import Flask
from flask_restplus import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app=app, version="1.0", doc="/atmos/api", title="AtmosApi", description="Api de gestion de l'AtmosBase", default="AtmosApi", default_label='AtmosApi', validate=True)
cors = CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')

################# MEASURES CLASSES #################
@api.route("/atmos/measure/<probe_id>")
class MeasureAll(Resource):
    def get(self, probe_id):
        """
        Print all measure of one probe
        :param probe_id:
        :return:
        """
        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s" % probe_id)
        ids = dbCursor.fetchall()
        MEASURES = []
        for i in range(1, len(ids) + 1):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]),
                             'date': sql_select_date(ids[i - 1])})
        return MEASURES

@api.route("/atmos/measure/<measure_id>")
class MeasureOne(Resource):
    def get(self, measure_id):
        """
        Print one measure
        :param measure_id:
        :return:
        """
        mesure = {'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id),
                  'date': sql_select_date(measure_id)}
        return mesure

    def delete(self, measure_id):
        """
        Delete one measure
        :param measure_id:
        :return:
        """
        dbCursor.execute("DELETE FROM 'MESURE' WHERE id_mesure= %d" % measure_id)

        return '', 204


@api.route("/atmos/measure/day/<probe_id>")
class MeasureDay(Resource):
    def get(self, probe_id):
        """
        Print all measure of last day
        :param probe_id:
        :return:
        """
        DateNow = datetime.today()
        DateBefore = DateNow - timedelta(days=1)
        DateNow = DateNow.strftime("%Y-%m-%d %H:%M:%S")
        DateBefore = DateBefore.strftime("%Y-%m-%d %H:%M:%S")

        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s and mesure_date between '%s' and '%s'" % (
            probe_id, DateBefore, DateNow))
        ids = dbCursor.fetchall()
        MEASURES = []
        for i in range(1, len(ids)):
            MEASURES.append({'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]),
                             'date': sql_select_date(ids[i - 1])})
        return MEASURES

@api.route("/atmos/measure/last/<probe_id>")
class MeasureLast(Resource):
    def get(self, probe_id):
        """
        Print last measure of one probe
        :param probe_id:
        :return:
        """

        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s ORDER BY id_mesure DESC LIMIT 1" % probe_id)
        lastId = dbCursor.fetchone()
        lastId = int(lastId[0])
        mesure = {'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId),
                  'date': sql_select_date(lastId)}
        return mesure

@api.route("/atmos/measure/add/<probe_id>/<temp>+<humidity>")
class MeasurePost(Resource):
    def post(self, temp, humidity, probe_id):
        """
        Add one measure in Database
        :param temp:
        :param humidity:
        :param probe_id:
        :return:
        """
        dateNow = datetime.today()
        dateNow = dateNow.strftime("%Y-%m-%d %H:%M:%S")

        values = {'temp': temp, 'humidite': humidity, 'date': dateNow}

        dbCursor.execute(
            "INSERT INTO MESURE (id_sonde, mesure_date, mesure_temp, mesure_humidite) VALUES (%s, '%s', %s, %s)" % (
                probe_id, dateNow, temp, humidity))
        atmosDB.commit()
        return values, 201


################## PROBES CLASSES ##################
@api.route("/atmos/probe/")
class ProbeList(Resource):
    def get(self):
        """
        List all probes
        :return:
        """
        dbCursor.execute("SELECT id_sonde FROM SONDE")
        ids = dbCursor.fetchall()
        PROBES = []
        for i in range(1, len(ids) + 1):
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

@api.route("/atmos/probe/add/<probe_name>+<latitude>+<longitude>+<measure_type>")
class ProbePost(Resource):
    def post(self, probe_name, latitude, longitude, measure_type):
        """
        Add a probe in Database
        :param probe_name:
        :param latitude:
        :param longitude:
        :param measure_type:
        :return:
        """
        values = {'name': probe_name, 'latitude': latitude, 'longitude': longitude}

        dbCursor.execute(
            "INSERT INTO SONDE (id_utilisateur, sonde_pos_latitude, sonde_pos_longitude, sonde_nom, sonde_active)"
            " VALUES (%s, %s, %s, '%s', 1)" % (
                1, latitude, longitude, probe_name))
        atmosDB.commit()

        dbCursor.execute("SELECT id_sonde FROM SONDE ORDER BY id_sonde DESC LIMIT 1")
        lastId = dbCursor.fetchone()
        lastId = int(lastId[0])

        return values, 201

@api.route("/atmos/probe/state/change/<probe_id>")
class ProbeChangeState(Resource):
    def put(self, probe_id):
        """
        Change state of one probe (active or not)
        :param probe_id:
        :return:
        """
        dbCursor.execute("SELECT sonde_active FROM SONDE WHERE id_sonde = %s" % probe_id)
        activity = dbCursor.fetchone()[0]

        if (activity == 1):
            dbCursor.execute("UPDATE SONDE SET sonde_active = 0 WHERE id_sonde = %s" % probe_id)
            atmosDB.commit()
        else:
            if (activity == 0):
                dbCursor.execute("UPDATE SONDE SET sonde_active = 1 WHERE id_sonde = %s" % probe_id)
                atmosDB.commit()

        return 'Updated', 200


##
# Actually setup the Api resource routing here
##
api.add_resource(MeasureAll, '/atmos/measure/<probe_id>')
api.add_resource(MeasureOne, '/atmos/measure/<measure_id>')
api.add_resource(MeasureDay, '/atmos/measure/day/<probe_id>')
api.add_resource(MeasureLast, '/atmos/measure/last/<probe_id>')
api.add_resource(MeasurePost, '/atmos/measure/add/<probe_id>/<temp>+<humidity>')

api.add_resource(ProbeList, '/atmos/probe/')
api.add_resource(ProbePost, '/atmos/probe/add/<probe_name>+<latitude>+<longitude>+<measure_type>')
api.add_resource(ProbeChangeState, '/atmos/probe/state/change/<probe_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
