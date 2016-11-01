from simplexml import dumps
from flask import make_response, Flask
from flask import Flask
from datetime import datetime
import json
from flask_restful import Resource, Api
from flask_restful import reqparse
from xml.etree import ElementTree
from flask.ext.mysql import MySQL


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response' :data}), code)
    resp.headers.extend(headers or {})
    return resp

app = Flask(__name__)
api = Api(app, default_mediatype='application/xml')
api.representations['application/xml'] = output_xml

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'provider_2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

class Notification(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='ID of specific notification')
            parser.add_argument('date', type=str, help='Notification date and time')
            parser.add_argument('street_number', type=int, help='Street number for specific notification')
            parser.add_argument('street_name', type=str, help='Notification full street name')
            parser.add_argument('city', type=str, help='Notification city name')
            parser.add_argument('customer_id', type=str, help='ID of caller who reported notification')
            parser.add_argument('description', type=str, help='Additional description of notification')

            args = parser.parse_args()

            _notificationId = args['id']
            _notificationDate = args['date']
            _notificationStreetNumber = args['street_number']
            _notificationStreetName = args['street_name']
            _notificationCity = args['city']
            _notificationCustomerId = args['customer_id']
            _notificationDescription = args['description']

            cursor.execute('SELECT * FROM notification WHERE id=\'%s\'' % args['id'])
            data = cursor.fetchall()
            print data
            print data[0]
            items_list = []
            for x in data:
                items_list.append({'notification': {
                    'id': data[0],
                    'date': str(data[1]),
                    'street_number': data[2],
                    'street_name': data[3],
                    'city': data[4],
                    'customer_id': data[5],
                    'description': data[6]
                    }})
        except Exception as e:
            return {'error': str(e)}

    def get(self):
        cursor.execute('SELECT * FROM notification')
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

class Caller(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, help='Caller ID unique code')
            parser.add_argument('name', type=str, help='Caller full name')
            parser.add_argument('phone_prefix', type=str, help='Caller phone prefix')
            parser.add_argument('phone_number', type=str, help='Caller phone number')
            args = parser.parse_args()

            _callerId = args['id']
            _callerName = args['name']
            _callerPhonePrefix = args['phone_prefix']
            _callerPhoneNumber= args['phone_number']

            cursor.execute('SELECT * FROM caller WHERE id=\'%s\'' % args['id'])
            data = cursor.fetchall()[0]

            return {
                'id': data[0],
                'name': data[1],
                'phone_prefix': data[2],
                'phone_number': data[3]
                }
        except Exception as e:
            return {'error': str(e)}

    def get(self):
        cursor.execute('SELECT * FROM caller')
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


api.add_resource(Notification, '/Notification')
api.add_resource(Caller, '/Caller')

if __name__ == '__main__':
    app.run(debug=True)
