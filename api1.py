#!/usr/bin/python
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


def output_xml(data, code, headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response' :data}), code)
    resp.headers.extend(headers or {})
    return resp

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')
api.representations['application/xml'] = output_xml

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'provider_1'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


class NotificationID(Resource):
    def get(self, url_id):
        if re.match('.*\*.*', url_id):
            url_id = url_id.replace('*', '%')
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
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationDATETIME(Resource):
    def get(self, url_date_time):
        if not re.match(
            '^[><]?\d{1,4}-?\d{0,2}-?\d{0,2}T?\d{0,2}:?\d{0,2}:?\d{0,2}$',
                url_date_time):
            return {
                'error': 'Invalid datetime format. Use YYYY-mm-ddThh:MM:SS'}
        try:
            operator = re.findall('([><])', url_date)[0]
        except IndexError:
            operator = '='

        date, time = self.parse_time(url_date_time)

        if not self.validate_time(time) or not self.validate_date(date):
            return {'error': 'Invalid datetime'}
        # return operator+date+'T'+time

        cursor.execute(
            'SELECT * FROM notification WHERE date_time %s \'%s %s\'' % (
                operator, date, time))

        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'notification': {
                'id': x[0],
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
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


class NotificationADDRESS(Resource):
    def get(self, url_address):
        url_address = ' '.join(url_street.split('_'))
        if re.match('.*\*.*', url_address):
            url_address = url_address.replace('*', '%')
            cursor.execute(
                'SELECT * FROM notification WHERE address LIKE \'%s\'' %
                url_address)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE address = \'%s\'' %
                url_address)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'notification': {
                'id': x[0],
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationCITY(Resource):
    def get(self, url_city):
        url_city = ' '.join(url_city.split('_'))
        if re.match('.*\*.*', url_city):
            url_city = url_city.replace('*', '%')
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
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationcallerID(Resource):
    def get(self, url_caller_id):
        if re.match('.*\*.*', url_caller_id):
            url_caller_id = url_caller_id.replace('*', '%')
            cursor.execute(
                'SELECT * FROM notification WHERE caller_id LIKE \'%s\'' %
                url_caller_id)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE caller_id = \'%s\'' %
                url_caller_id)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'notification': {
                'id': x[0],
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class NotificationADDITIONALINFORMATION(Resource):
    def get(self, url_add_info):
        url_add_info = ' '.join(url_add_info.split('_'))
        if re.match('.*\*.*', url_add_info):
            url_add_info = url_add_info.replace('*', '%')
            cursor.execute(
                'SELECT * FROM notification WHERE additional_information LIKE \'%s\'' %
                url_add_info)
        else:
            cursor.execute(
                'SELECT * FROM notification WHERE additional_information = \'%s\'' %
                url_add_info)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'notification': {
                'id': x[0],
                'date_time': str(x[1]),
                'address': x[2],
                'city': x[3],
                'caller_id': x[4],
                'additional_information': x[5]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerID(Resource):
    def get(self, url_id):
        if re.match('.*\*.*', url_id):
            url_id = url_id.replace('*', '%')
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
                'last_name': x[2],
                'phone': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerNAME(Resource):
    def get(self, url_name):
        url_name = ' '.join(url_name.split('_'))
        if re.match('.*\*.*', url_name):
            url_name = url_name.replace('*', '%')
            cursor.execute(
                'SELECT * FROM caller WHERE name LIKE \'%s\'' %
                url_name)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE name = \'%s\'' %
                url_name)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'last_name': x[2],
                'phone': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerLASTNAME(Resource):
    def get(self, url_last_name):
        if re.match('.*\*.*', url_last_name):
            url_last_name = url_last_name.replace('*', '%')
            cursor.execute(
                'SELECT * FROM caller WHERE last_name LIKE \'%s\'' %
                url_last_name)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE last_name = \'%s\'' %
                url_last_name)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'last_name': x[2],
                'phone': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


class CallerPHONE(Resource):
    def get(self, url_phone):
        if re.match('.*\*.*', url_phone):
            url_phone = url_phone.replace('*', '%')
            cursor.execute(
                'SELECT * FROM caller WHERE phone LIKE \'%s\'' %
                url_phone)
        else:
            cursor.execute(
                'SELECT * FROM caller WHERE phone = \'%s\'' %
                url_phone)
        data = cursor.fetchall()
        items_list = []
        for x in data:
            items_list.append({'caller': {
                'id': x[0],
                'name': x[1],
                'last_name': x[2],
                'phone': x[3]
            }})
        return {'items': items_list, 'items_count': len(items_list)}


api.add_resource(NotificationID,
                 '/notification/id/<string:url_id>')
api.add_resource(NotificationDATETIME,
                 '/notification/date_time/<string:url_date_time>')
api.add_resource(NotificationADDRESS,
                 '/notification/address/<string:url_address>')
api.add_resource(NotificationCITY,
                 '/notification/city/<string:url_city>')
api.add_resource(NotificationcallerID,
                 '/notification/callerid/<string:url_caller_id>')
api.add_resource(NotificationADDITIONALINFORMATION,
                 '/notification/add_information/<string:add_info>')

api.add_resource(CallerID,
                 '/caller/id/<string:url_id>')
api.add_resource(CallerNAME,
                 '/caller/name/<string:url_name>')
api.add_resource(CallerLASTNAME,
                 '/caller/last_name/<string:url_last_name>')
api.add_resource(CallerPHONE,
                 '/caller/phone/<string:url_phone>')

if __name__ == '__main__':
    app.run(port='1111')
