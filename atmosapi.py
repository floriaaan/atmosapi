import pymysql
from flask import Flask, request
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app=app, version='0.1', title='Atmos Api', description='', validate=True)



atmosDB = pymysql.connect(
    host="127.0.0.1",
    user="atmosfr",
    passwd="atmosfr",
    charset="utf8",
    db="atmosfr"

)

dbCursor = atmosDB.cursor()


ns_measures = api.namespace('measures', description = "Measures")
ns_probes = api.namespace('probes', description = "Probes")



@ns_measures.route("/atmos/measures")
class MeasureList(Resource):
    def get(self):
        """
        returns a list of Measures
        """
        cursor = atmosDB.Measures.find({}, {"_id": 0})
        data = []
        for measure in cursor:
            data.append(measure)
        return {"response": data}


    def post(self):
        """
        Add a new Measure to the list
        """
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return data, 404
        else:
            title = data.get('title')
            if title:
                atmosDB.insert(data)



@ns_probes.route("/atmos/probes")
class ProbesList(Resource):
    def put(self, title):
        """
        Edits a selected probe
        """
        data = request.get_json()
        atmosDB.Probes.update({'title': title}, {'set': data})


    def delete(self, title):
        """
        delete a selected book
        """
        atmosDB.Probes.delete({'title': title})