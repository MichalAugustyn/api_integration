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

class NotificationDATE(Resource):
    def get(self, url_date):

        date, time = self.parse_time(url_date)

        if not self.validate_time(time) or not self.validate_date(date):
            return {'error': 'Invalid datetime'}
        print date+'T'+time

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

    def parse_time(self,url_date):
        split_date = url_date.split('T')

        date = split_date[0] if len(split_date) > 0 else '1900-01-01'
        time = split_date[1] if len(split_date) > 1 else '00:00:00'

        date_list = re.findall('\d+', date)
        time_list = re.findall('\d+', time)

        year = date_list[0] if len(date_list) > 0  else '1900'
        month = date_list[1] if len(date_list) > 1 else '01'
        day = date_list[2] if len(date_list) > 2 else '01'
        hour = time_list[0] if len(time_list) > 0 else '00'
        minute = time_list[1] if len(time_list) > 1 else '00'
        second = time_list[2] if len(time_list) > 2 else '00'

        date = '%s-%s-%s' % (year, month, day)
        time = '%s:%s:%s' % (hour, minute, second)
        return date, time

        # date = url_date().split()[0]
        # try:
        #     time = url_date().split()[1]
        # except ValueError:
        #     time = '00:00:00'

        # if re.match('^>.*', url_date):
        #     print 'SELECT * FROM notification WHERE date>%s %s' % (date, time)
        #     cursor.execute('SELECT * FROM notification WHERE date%s %s' % (date, time))
        # if re.match('^<.*', url_date):
        #     cursor.execute('SELECT * FROM notification WHERE date<%s' % url_date)
        # else:
        #     cursor.execute('SELECT * FROM notification WHERE date=%s' % url_date)
        # data = cursor.fetchall()
        # items_list = []
        # xml_items_list = []
        # for x in data:
        #     items_list.append({'notification': {
        #         'id': x[0],
        #         'date': str(x[1]),
        #         'street_number': x[2],
        #         'street_name': x[3],
        #         'city': x[4],
        #         'customer_id': x[5],
        #         'description': x[6]
        #         }})
        # return items_list

class CallerID(Resource):
    def get(self, url_id):
        if re.match('.*>.*', url_date):
            cursor.execute('SELECT * FROM caller WHERE date>\'%s\'' % url_date)
        if re.match('.*<.*', url_date):
            cursor.execute('SELECT * FROM caller WHERE date<\'%s\'' % url_date)
        else:
            cursor.execute('SELECT * FROM caller WHERE date=\'%s\'' % url_date)
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


api.add_resource(NotificationID, '/Notification/id/<string:url_id>')
api.add_resource(NotificationDATE, '/Notification/date/<string:url_date>')
api.add_resource(CallerID, '/Caller/<string:url_id>')

if __name__ == '__main__':
    app.run(debug=True)