from simplexml import dumps
from flask import make_response, Flask
from flask import Flask
from datetime import datetime
import json
import re
from flask_restful import Resource, Api
from flask_restful import reqparse
from xml.etree import ElementTree
from flask.ext.mysql import MySQL


# def output_xml(data, code, headers=None):
#     """Makes a Flask response with a XML encoded body"""
#     resp = make_response(dumps({'response' :data}), code)
#     resp.headers.extend(headers or {})
#     return resp

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')
# api.representations['application/xml'] = output_xml

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'provider_2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

class NotificationID(Resource):

    def get(self, url_id):
        if re.match('.*%.*', url_id):
            cursor.execute('SELECT * FROM notification WHERE id like \'%s\'' % url_id)
        else:
            cursor.execute('SELECT * FROM notification WHERE id=\'%s\'' % url_id)
        data = cursor.fetchall()
        items_list = []
        xml_items_list = []
        for x in data:
            items_list.append({'notification': {
                'id': x[0],
                'date': str(x[1]),
                'street_number': x[2],
                'street_name': x[3],
                'city': x[4],
                'customer_id': x[5],
                'description': x[6]
                }})
        return items_list

class CallerID(Resource):

    def get(self, url_id):
        cursor.execute('SELECT * FROM caller WHERE id=\'%s\'' % url_id)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append( {
                'id': x[0],
                'name': x[1],
                'phone_prefix': x[2],
                'phone_number': x[3]
                })
        return items_list


api.add_resource(NotificationID, '/Notification/<string:url_id>')
api.add_resource(CallerID, '/Caller/<string:url_id>')

if __name__ == '__main__':
    app.run(debug=True)
