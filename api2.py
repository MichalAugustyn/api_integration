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
            cursor.execute(
                'SELECT * FROM notification WHERE id LIKE \'%s\'' % url_id)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE id = \'%s\'' % url_id)
        data = cursor.fetchall()
        items_list = []
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
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationDATE(Resource):
    def get(self, url_date):
        if not re.match(
            '^[><]?\d{1,4}-?\d{0,2}-?\d{0,2}T?\d{0,2}:?\d{0,2}:?\d{0,2}$',
                url_date):
            return {
                'error': 'Invalid datetime format. Use YYYY-mm-ddThh:MM:SS'}
        try:
            operator = re.findall('([><])', url_date)[0]
        except IndexError:
            operator = '='

        date, time = self.parse_time(url_date)

        if not self.validate_time(time) or not self.validate_date(date):
            return {'error': 'Invalid datetime'}
        # return operator+date+'T'+time

        cursor.execute(
            'SELECT * FROM notification WHERE date %s \'%s %s\'' % (
                operator, date, time))

        data = cursor.fetchall()
        items_list = []
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
        print date, time
        return {'items': items_list, 'items_count': len(items_list)}

    def validate_date(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_time(self, time):
        try:
            datetime.strptime(time, '%H:%M:%S')
            return True
        except ValueError:
            return False

    def parse_time(self, url_date):
        datetime_list = re.findall('\d+', url_date)

        if datetime_list == []:
            return 'invalid', 'datetime'

        year = datetime_list[0] if len(datetime_list) > 0 else '1900'
        month = datetime_list[1] if len(datetime_list) > 1 else '01'
        day = datetime_list[2] if len(datetime_list) > 2 else '01'
        hour = datetime_list[3] if len(datetime_list) > 3 else '00'
        minute = datetime_list[4] if len(datetime_list) > 4 else '00'
        second = datetime_list[5] if len(datetime_list) > 5 else '00'

        date = '%0.4d-%0.2d-%0.2d' % (int(year), int(month), int(day))
        time = '%0.2d:%0.2d:%0.2d' % (int(hour), int(minute), int(second))
        return date, time


class NotificationSTREET(Resource):
    def get(self, url_street):
        url_street = ' '.join(url_street.split('_'))
        if re.match('.*%.*', url_street):
            cursor.execute(
                'SELECT * FROM notification WHERE street_name LIKE \'%s\'' %
                url_street)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE street_name = \'%s\'' %
                url_street)
        data = cursor.fetchall()
        items_list = []
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
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationCITY(Resource):
    def get(self, url_city):
        url_city = ' '.join(url_city.split('_'))
        if re.match('.*%.*', url_city):
            cursor.execute(
                'SELECT * FROM notification WHERE city LIKE \'%s\'' % url_city)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE city = \'%s\'' % url_city)
        data = cursor.fetchall()
        items_list = []
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
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationCUSTOMERID(Resource):
    def get(self, url_customer_id):
        if re.match('.*%.*', url_customer_id):
            cursor.execute(
                'SELECT * FROM notification WHERE customer_id LIKE \'%s\'' %
                url_customer_id)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE customer_id = \'%s\'' %
                url_customer_id)
        data = cursor.fetchall()
        items_list = []
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
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationDESCRIPTION(Resource):
    def get(self, url_description):
        url_description = ' '.join(url_description.split('_'))
        if re.match('.*%.*', url_description):
            cursor.execute(
                'SELECT * FROM notification WHERE description LIKE \'%s\'' %
                url_description)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE description = \'%s\'' %
                url_description)
        data = cursor.fetchall()
        items_list = []
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
        return {'items': items_list, 'items_count': len(items_list)}


class CallerID(Resource):
    def get(self, url_id):
        if re.match('.*%.*', url_id):
            cursor.execute(
                'SELECT * FROM caller WHERE id LIKE \'%s\'' % url_id)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE id = \'%s\'' % url_id)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'phone_prefix': x[2],
                'phone_number': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerNAME(Resource):
    def get(self, url_name):
        url_name = ' '.join(url_name.split('_'))
        if re.match('.*%.*', url_name):
            cursor.execute(
                'SELECT * FROM caller WHERE street_name LIKE \'%s\'' %
                url_name)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE street_name = \'%s\'' %
                url_name)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'phone_prefix': x[2],
                'phone_number': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerPHONEPREFIX(Resource):
    def get(self, url_phone_prefix):
        if re.match('.*%.*', url_phone_prefix):
            cursor.execute(
                'SELECT * FROM caller WHERE phone_prefix LIKE \'%s\'' %
                url_phone_prefix)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE phone_prefix = \'%s\'' %
                url_phone_prefix)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'phone_prefix': x[2],
                'phone_number': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerPHONENUMBER(Resource):
    def get(self, url_phone_number):
        if re.match('.*%.*', url_phone_number):
            cursor.execute(
                'SELECT * FROM caller WHERE phone_number LIKE \'%s\'' %
                url_phone_number)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE phone_number = \'%s\'' %
                url_phone_number)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'phone_prefix': x[2],
                'phone_number': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}
api.add_resource(NotificationID,
                 '/notification/id/<string:url_id>')
api.add_resource(NotificationDATE,
                 '/notification/date/<string:url_date>')
api.add_resource(NotificationSTREET,
                 '/notification/street/<string:url_street>')
api.add_resource(NotificationCITY,
                 '/notification/city/<string:url_city>')
api.add_resource(NotificationCUSTOMERID,
                 '/notification/customerid/<string:url_customer_id>')
api.add_resource(NotificationDESCRIPTION,
                 '/notification/description/<string:url_description>')

api.add_resource(CallerID,
                 '/caller/id/<string:url_id>')
api.add_resource(CallerNAME,
                 '/caller/name/<string:url_name>')
api.add_resource(CallerPHONEPREFIX,
                 '/caller/phone_prefix/<string:url_phone_prefix>')
api.add_resource(CallerPHONENUMBER,
                 '/caller/phone_number/<string:url_phone_number>')

if __name__ == '__main__':
    app.run(port='2222')