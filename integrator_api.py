#!/usr/bin/python
from simplexml import loads
from flask import make_response, Flask
from flask import Flask
from datetime import datetime
import json
import requests
import re
from flask_restful import Resource, Api
from flask_restful import reqparse
from xml.etree import ElementTree
from flask.ext.mysql import MySQL
from time import sleep

app = Flask(__name__)
api = Api(app, default_mediatype='application/json')


@api.resource('/notification')
class Notification(Resource):
    def get(self):
        return integrate_items()


@api.resource('/notification/id/<string:url_id>')
class NotificationID(Resource):
    def get(self, url_id):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['id'])]


@api.resource('/notification/date/<string:url_date>')
class NotificationDATE(Resource):
    def get(self, url_date):
        # datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S')

        try:
            operator = re.findall('[><]?', url_date)[0][0]
        except IndexError:
            operator = '='
        try:
            date = re.findall('^[><]?([\d:-T]*)', url_date)[0][1]
            date_formatted = self.parse_time(url_date)
            datetime.strptime(date_formatted, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, IndexError):
            return {'error': 'Invalid data format. Use %Y-%m-%dT%H:%M:%S',
                'hint': 'It is allowed to provide incomplete data (%Y, %Y-%m, etc'}

        return {'date': date_formatted, 'operator': operator}


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
        # return datetime.strptime(date + 'T' + time, '%Y-%m-%dT%H:%M:%S')
        return date + 'T' + time

@api.resource('/notification/street/<string:url_street>')
class NotificationSTREET(Resource):
    def get(self, url_street):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['street_name'])]


@api.resource('/notification/city/<string:url_city>')
class NotificationCITY(Resource):
    def get(self, url_city):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['city'])]


@api.resource('/notification/description/<string:url_description>')
class NotificationDESCRIPTION(Resource):
    def get(self, url_description):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['description'])]


@api.resource('/caller/name/<string:url_name>')
class CallerNAME(Resource):
    def get(self, url_name):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['name'])]


@api.resource('/caller/name/<string:url_name>')
class CallerLASTNAME(Resource):
    def get(self, url_name):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['last_name'])]


@api.resource('/caller/phone_prefix/<string:url_phone_prefix>')
class CallerPHONEPREFIX(Resource):
    def get(self, url_phone_prefix):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['phone_prefix'])]


@api.resource('/caller/phone_number/<string:url_phone_number>')
class CallerPHONENUMBER(Resource):
    def get(self, url_phone_number):
        return [
            x 
            for x in integrate_items() 
            if re.match(url_id, x['phone_number'])]

 
def integrate_items():
        provider_1_request = requests.get('http://localhost:1111/notification')
        provider_2_request = requests.get('http://localhost:2222/notification')
        provider_1_items = loads(json.loads(provider_1_request.text))['response']
        provider_1_integrated = [{
            'id': x['id'],
            'date': x['date_time'],
            'name': x['name'].capitalize(),
            'last_name': x['last_name'].capitalize(),
            'phone_prefix': int(re.findall('\((\d+)\)', x['phone'])[0]),
            'phone_number': int("".join(re.findall('(\d+)-(\d+)', x['phone'])[0])),
            'street_number': int(re.findall('(\d+) (.+)', x['address'])[0][0]),
            'street_name': re.findall('(\d+) (.+)', x['address'])[0][1],
            'city': x['city'],
            'description': x['additional_information'].capitalize()
            } for x in provider_1_items['items'] ]

        provider_2_items = json.loads(provider_2_request.text)
        provider_2_integrated = [{
            'id': x['id'],
            'date': x['date'],
            'name': x['name'].split()[0],
            'last_name': x['name'].split()[1].capitalize(),
            'phone_prefix': x['phone_prefix'],
            'phone_number': x['phone_number'],
            'street_number': x['street_number'],
            'street_name': x['street_name'],
            'city': x['city'],
            'description': x['description'].capitalize()
            } for x in provider_2_items['items']]
        items_list = sorted(provider_2_integrated + provider_1_integrated,
            key=lambda x: x['date'])
        return {'items': items_list, 'items_count': len(items_list)}

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3333)
