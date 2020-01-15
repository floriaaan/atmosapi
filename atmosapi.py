import pymysql
from flask import Flask
from flask_restplus import reqparse, Api, Resource, fields
from flask_cors import CORS

from datetime import datetime
from datetime import timedelta
import json

try:
    atmosDB = pymysql.connect(
        host="127.0.0.1",
        user="atmos",
        passwd="atmos",
        charset="utf8",
        db="atmos"
    )
    dbCursor = atmosDB.cursor()
except:
    print("Connection failed!")



def sql_select_date(id):
    try:
        dbCursor.execute("SELECT mesure_date FROM MESURE WHERE id_mesure='%s'" % id)
        date = dbCursor.fetchall()
        returndate = date[0][0].strftime("%Y-%m-%d %H:%M:%S")
        return returndate
    except:
        print("exception!")
        return None


def sql_select_temp(id):
    try:
        dbCursor.execute("SELECT mesure_temp FROM MESURE WHERE id_mesure='%s'" % id)
        temp = json.dumps(dbCursor.fetchone()[0])
        return temp
    except:
        print("exception!")
        return None


def sql_select_humid(id):
    try:
        dbCursor.execute("SELECT mesure_humidite FROM MESURE WHERE id_mesure='%s'" % id)
        humid = json.dumps(dbCursor.fetchone()[0])
        return humid
    except:
        print("exception!")
        return None




app = Flask(__name__)

api = Api(app=app,
          version="1.0",
          doc="/atmos/api",
          title="AtmosApi",
          default="AtmosAPI",
          default_label="API de l'AtmosBase",
          contact="Florian Leroux",
          contact_email="florian.leroux@viacesi.fr",
          contact_url="https://github.com/floriaaan/",
          description="Actions related to interactions with AtmosBase",
          validate=True)
cors = CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidite')
parser.add_argument('date')


ns_measure = api.namespace('Measures', description= "Actions related to measures", path="/")

################# MEASURES CLASSES #################
@ns_measure.route("/atmos/measure/<int:probe_id>")
class MeasureAll(Resource):
    @api.response(200, 'Measures : Measures obtained')
    @api.response(400, 'Measures : Error')
    @api.response(403, 'Measures : Error, forbidden access')
    def get(self, probe_id):
        """
        Print all measure of one probe
        :param probe_id:
        :return:
        """
        MEASURES = []
        try:
            dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s" % probe_id)
            ids = dbCursor.fetchall()

            for i in range(1, len(ids) + 1):
                MEASURES.append({'probe_id': probe_id, 'measure_id' : (i - 1), 'temp': sql_select_temp(ids[i - 1]), 'humidite': sql_select_humid(ids[i - 1]),
                                 'date': sql_select_date(ids[i - 1]), 'error': {'flag': False}})
        except Exception as e:
            MEASURES = {'probe_id': probe_id, 'error' : {'flag': True, 'type' : json.dumps(str(e))}}
        return MEASURES, 200

@ns_measure.route("/atmos/measure/one/<int:measure_id>")
class MeasureOne(Resource):
    @api.response(200, 'Measure : Measure obtained')
    @api.response(400, 'Measure : Error')
    @api.response(403, 'Measure : Error, forbidden access')
    def get(self, measure_id):
        """
        Print one measure
        :param measure_id:
        :return:
        """
        mesure = {}
        try:
            mesure = {'measure_id' : measure_id, 'temp': sql_select_temp(measure_id), 'humidite': sql_select_humid(measure_id),
                      'date': sql_select_date(measure_id), 'error': {'flag': False}}
        except Exception as e:
            mesure = {'measure_id' : measure_id, 'error' : {'flag': True, 'type' : json.dumps(str(e))}}
            return mesure, 400
        return mesure, 200

    @api.response(204, 'Measure : Measure deleted')
    @api.response(400, 'Measure : Error')
    @api.response(403, 'Measure : Error, forbidden access')
    def delete(self, measure_id):
        """
        Delete one measure
        :param measure_id:
        :return:
        """
        try:
            dbCursor.execute("DELETE FROM MESURE WHERE id_mesure= %s" % measure_id)
            #dbCursor.execute("SET @num := 0")
            #dbCursor.execute("UPDATE MESURE SET id_mesure = @num := (@num+1)")
            dbCursor.execute("ALTER TABLE MESURE AUTO_INCREMENT = 1")
            atmosDB.commit()
        except Exception as e:
            return {'error': {'flag': True, 'type' : json.dumps(str(e))}}, 400



        return {'error': False}, 204

@ns_measure.route("/atmos/measure/day/<probe_id>")
class MeasureDay(Resource):
    @api.response(200, 'Measures : Day\'s values obtained')
    @api.response(400, 'Measures : Error')
    @api.response(403, 'Measures : Error, forbidden access')
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

        MEASURES = []

        dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s and mesure_date between '%s' and '%s'" % (
            probe_id, DateBefore, DateNow))
        ids = dbCursor.fetchall()

        for i in range(0, len(ids)):
            MEASURES.append({'probe_id' : probe_id, 'temp': sql_select_temp(ids[i]), 'humidite': sql_select_humid(ids[i]),
                             'date': sql_select_date(ids[i]), 'error' : {'flag': False}})

        return MEASURES, 200

@ns_measure.route("/atmos/measure/last/<probe_id>")
class MeasureLast(Resource):
    @api.response(200, 'Measure : Measure obtained')
    @api.response(400, 'Measure : Error')
    @api.response(403, 'Measure : Error, forbidden access')
    def get(self, probe_id):
        """
        Print last measure of one probe
        :param probe_id:
        :return:
        """
        try:
            dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s ORDER BY id_mesure DESC LIMIT 1" % probe_id)
            lastId = dbCursor.fetchone()
            lastId = int(lastId[0])
            mesure = {'probe_id' : probe_id, 'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId),
                      'date': sql_select_date(lastId), 'error': {'flag': False}}
        except Exception as e:
            mesure = {'probe_id' : probe_id, 'error' : {'flag': True, 'type' : json.dumps(str(e))}}
            return mesure, 400
        return mesure, 200


@ns_measure.route("/atmos/measure/last/all")
class MeasureLastAllProbes(Resource):
    @api.response(200, 'Measures : Measures obtained')
    @api.response(400, 'Measures : Error')
    @api.response(403, 'Measures : Error, forbidden access')
    def get(self):
        """
        Print last measure of all probe
        :return:
        """

        dbCursor.execute("SELECT id_sonde FROM SONDE")
        ids = dbCursor.fetchall()



        MEASURES = []
        for i in range(0, len(ids)):


            dbCursor.execute("SELECT id_mesure FROM MESURE WHERE id_sonde = %s ORDER BY id_mesure DESC LIMIT 1" % ids[i])
            lastId = dbCursor.fetchone()

            if(lastId != None):
                lastId = int(lastId[0])
                MEASURES.append({'probe_id' : i,'temp': sql_select_temp(lastId), 'humidite': sql_select_humid(lastId),
                                         'date': sql_select_date(lastId), 'error': {'flag': False}})
            else:
                MEASURES.append({'probe_id' : i, 'error': {'flag': True}})



        return MEASURES, 200


measure_post = api.model('Measure Post Informations', {
    'probe_id': fields.Integer(required=True),
    'temp': fields.Float(required=True),
    'humidity': fields.Float(required=True)
})

@ns_measure.route("/atmos/measure/add/")
class MeasurePost(Resource):
    @api.response(201, 'Measure : Measure added')
    @api.response(400, 'Measure : Error')
    @api.response(403, 'Measure : Error, forbidden access')

    @api.expect(measure_post)
    def post(self):
        """
        Add one measure in Database
        :param temp:
        :param humidity:
        :param probe_id:
        :return:
        """
        probe_id = api.payload['probe_id']

        temp = api.payload['temp']
        humidity = api.payload['humidity']


        dateNow = datetime.today()
        dateNow = dateNow.strftime("%Y-%m-%d %H:%M:%S")

        values = {'temp': temp, 'humidite': humidity, 'date': dateNow}
        dbCursor.execute(
        "INSERT INTO MESURE (id_sonde, mesure_date, mesure_temp, mesure_humidite) VALUES (%s, '%s', %s, %s)"
        % (probe_id, dateNow, temp, humidity))
        atmosDB.commit()
        return values, 201



ns_probe = api.namespace('Probes', description= "Actions related to probes", path="/")

################## PROBES CLASSES ##################
@ns_probe.route("/atmos/probe/")
class ProbeList(Resource):
    @api.response(200, 'Probes : List of all probes obtained')
    @api.response(400, 'Probes : Error')
    @api.response(403, 'Probes : Error, forbidden access')
    def get(self):
        """
        List all probes
        :return:
        """
        dbCursor.execute("SELECT id_sonde FROM SONDE")
        ids = dbCursor.fetchall()
        PROBES = []

        for i in range(1, len(ids) + 1):
            try:
                dbCursor.execute("SELECT id_utilisateur FROM SONDE WHERE id_sonde=%d" % i)
                user = json.dumps(dbCursor.fetchone()[0])

                dbCursor.execute("SELECT sonde_pos_latitude FROM SONDE WHERE id_sonde=%d" % i)
                pos_x = json.dumps(dbCursor.fetchone()[0])

                dbCursor.execute("SELECT sonde_pos_longitude FROM SONDE WHERE id_sonde=%d" % i)
                pos_y = json.dumps(dbCursor.fetchone()[0])

                dbCursor.execute("SELECT sonde_nom FROM SONDE WHERE id_sonde=%d" % i)
                name = json.dumps(dbCursor.fetchone()[0])

                dbCursor.execute("SELECT sonde_active FROM SONDE WHERE id_sonde=%d" % i)
                active = json.dumps(dbCursor.fetchone()[0])

                PROBES.append({'id': (i - 1), 'user': user, 'pos_x': pos_x, 'pos_y': pos_y, 'name': name, 'active': active, 'error' : {'flag': False}})
            except Exception as e:
                PROBES.append({'id': (i - 1), 'error' : {'flag': True, 'type' : json.dumps(str(e))}})


        return PROBES, 200





probe_post = api.model('Probe Post Informations', {
    'probe_name': fields.String(required=True),
    'latitude': fields.Float(),
    'longitude': fields.Float()
})

@ns_probe.route("/atmos/probe/add/")
class ProbePost(Resource):
    @api.response(201, 'Probe : Probe added')
    @api.response(400, 'Probe : Error')
    @api.response(403, 'Probe : Error, forbidden access')
    @api.expect(probe_post)
    def post(self):
        """
        Add a probe in Database
        :param probe_name:
        :param latitude:
        :param longitude:
        :return:
        """
        probe_name = api.payload['probe_name']
        if(api.payload['latitude'] != "null"):
            latitude = api.payload['latitude']
        else:
            latitude = "null"


        if(api.payload['longitude'] != "null"):
            longitude = api.payload['longitude']
        else:
            longitude = "null"

        values = {'name': probe_name, 'latitude': latitude, 'longitude': longitude}

        dbCursor.execute(
            "INSERT INTO SONDE (id_utilisateur, sonde_pos_latitude, sonde_pos_longitude, sonde_nom, sonde_active)"
            " VALUES (%s, %s, %s, '%s', 1)" % (
                1, latitude, longitude, probe_name))


        atmosDB.commit()


        return values, 201

@ns_probe.route("/atmos/probe/state/change/<int:probe_id>")
class ProbeChangeState(Resource):
    @api.response(200, 'Probe : State of probe changed')
    @api.response(400, 'Probe : Error')
    @api.response(403, 'Probe : Erreur, forbidden access')
    def put(self, probe_id):
        """
        Change state of one probe (active or not)
        :param probe_id:
        :return:
        """
        try:
            dbCursor.execute("SELECT sonde_active FROM SONDE WHERE id_sonde = %s" % probe_id)
            activity = dbCursor.fetchone()[0]
            if (activity == 1):
                dbCursor.execute("UPDATE SONDE SET sonde_active = 0 WHERE id_sonde = %s" % probe_id)
                atmosDB.commit()
                state = "unactive"
            elif (activity == 0):
                dbCursor.execute("UPDATE SONDE SET sonde_active = 1 WHERE id_sonde = %s" % probe_id)
                atmosDB.commit()
                state = "active"
        except Exception as e:
            return {'probe_id': probe_id, 'state': "undefined", 'error': {'flag': True, 'type' : json.dumps(str(e))}}, 400


        return {'probe_id': probe_id, 'state': state, 'error': {'flag': False}}, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0")
