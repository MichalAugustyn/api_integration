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

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'provider_2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
basic_sql = 'SELECT * FROM notification, caller WHERE notification.caller_id = caller.id '


@api.resource('/notification')
class Notification(Resource):
    def get(self):
        cursor.execute(basic_sql)
        return create_response(cursor.fetchall())


@api.resource('/notification/id/<string:url_id>')
class NotificationID(Resource):
    def get(self, url_id):
        if re.match('.*\*.*', url_id):
            url_id = url_id.replace('*', '%')
            cursor.execute(
                basic_sql + 'and notification.id LIKE \'%s\'' % url_id)
        else:
            cursor.execute(
                basic_sql + 'and notification.id = \'%s\'' % url_id)
        return create_response(cursor.fetchall())


@api.resource('/notification/date/<string:url_date>')
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

        cursor.execute(
            basic_sql + 'and notification.date %s \'%s %s\'' % (
                operator, date, time))
        return create_response(cursor.fetchall())

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

@api.resource('/notification/street/<string:url_street>')
class NotificationSTREET(Resource):
    def get(self, url_street):
        url_street = ' '.join(url_street.split('_'))
        if re.match('.*\*.*', url_street):
            url_street = url_street.replace('*', '%')
            cursor.execute(
                basic_sql + 'and notification.street_name LIKE \'%s\'' %
                url_street)
        else:
            cursor.execute(
                basic_sql + 'and notification.street_name = \'%s\'' %
                url_street)
        return create_response(cursor.fetchall())


@api.resource('/notification/city/<string:url_city>')
class NotificationCITY(Resource):
    def get(self, url_city):
        url_city = ' '.join(url_city.split('_'))
        if re.match('.*\*.*', url_city):
            url_city = url_city.replace('*', '%')
            cursor.execute(
                basic_sql + 'and notification.city LIKE \'%s\'' % url_city)
        else:
            cursor.execute(
                basic_sql + 'and notification.city = \'%s\'' % url_city)
        return create_response(cursor.fetchall())


@api.resource('/notification/callerid/<string:url_caller_id>')
class NotificationCALLERID(Resource):
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
        return create_response(cursor.fetchall())


@api.resource('/notification/description/<string:url_description>')
class NotificationDESCRIPTION(Resource):
    def get(self, url_description):
        url_description = ' '.join(url_description.split('_'))
        if re.match('.*\*.*', url_description):
            url_description = url_description.replace('*', '%')
            cursor.execute(
                basic_sql + 'and notification.description LIKE \'%s\'' %
                url_description)
        else:
            cursor.execute(
                basic_sql + 'and notification.description = \'%s\'' %
                url_description)
        return(create_response(cursor.fetchall()))


@api.resource('/caller/id/<string:url_id>')
class CallerID(Resource):
    def get(self, url_id):
        if re.match('.*\*.*', url_id):
            url_id = url_id.replace('*', '%')
            cursor.execute(
                basic_sql + 'and caller.id LIKE \'%s\'' % url_id)
        else:
            cursor.execute(
                basic_sql + 'and caller.id = \'%s\'' % url_id)
        return create_response(cursor.fetchall())


@api.resource('/caller/name/<string:url_name>')
class CallerNAME(Resource):
    def get(self, url_name):
        url_name = ' '.join(url_name.split('_'))
        if re.match('.*\*.*', url_name):
            url_name = url_name.replace('*', '%')
            cursor.execute(
                basic_sql + 'and caller.name LIKE \'%s\'' %
                url_name)
        else:
            cursor.execute(
                basic_sql + 'and caller.name = \'%s\'' %
                url_name)
        return create_response(cursor.fetchall())


@api.resource('/caller/phone_prefix/<string:url_phone_prefix>')
class CallerPHONEPREFIX(Resource):
    def get(self, url_phone_prefix):
        if re.matchix('.*\*.*', url_phone_prefix):
            url_phone_prefix = url_phone_prefix.replace('*', '%')
            cursor.execute(
                basic_sql + 'and caller.phone_prefix LIKE \'%s\'' %
                url_phone_prefix)
        else:
            cursor.execute(
                basic_sql + 'and caller.phone_prefix = \'%s\'' %
                url_phone_prefix)
        return create_response(cursor.fetchall())


@api.resource('/caller/phone_number/<string:url_phone_number>')
class CallerPHONENUMBER(Resource):
    def get(self, url_phone_number):
        if re.match('.*\*.*', url_phone_number):
            url_phone_number = url_phone_number.replace('*', '%')
            cursor.execute(
                basic_sql + 'and caller.phone_number LIKE \'%s\'' %
                url_phone_number)
        else:
            cursor.execute(
                basic_sql + 'and caller.phone_number = \'%s\'' %
                url_phone_number)
        return create_response(cursor.fetchall()) 

def create_response(data):
        items_list = []
        for x in data:
            items_list.append({
                'id': x[0],
                'date': str(x[1]),
                'street_number': x[2],
                'street_name': x[3],
                'city': x[4],
                'caller_id': x[5],
                'description': x[6],
                'name': x[8],
                'phone_prefix': x[9],
                'phone_number': x[10]
            })

        return {'items': items_list, 'items_count': len(items_list)}

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=2222)
