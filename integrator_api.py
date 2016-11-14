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
        return integrate_items()['items']

    def post(self):
        def argument_add(argument, parser):
            parser.add_argument(argument, type=str)
            arg = parser.parse_args()
            return arg[argument]

        def define_filters():
            filters = []
            filters.append(lambda n: re.match(_id, n['id'], re.IGNORECASE)) if _id else None
            filters.append(lambda n: re.match(_name, n['name'], re.IGNORECASE)) if _name else None
            filters.append(lambda n: datetime.strptime(
                _after, '%Y-%m-%dT%H:%M:%S') < datetime.strptime(
                n['date'], '%Y-%m-%d %H:%M:%S')) if _after else None
            filters.append(lambda n: datetime.strptime(
                _before, '%Y-%m-%dT%H:%M:%S') > datetime.strptime(
                n['date'], '%Y-%m-%d %H:%M:%S')) if _before else None
            filters.append(lambda n: re.match(_last_name, n['last_name'], re.IGNORECASE)) if _last_name else None
            filters.append(lambda n: re.match(_phone_prefix, str(n['phone_prefix'], re.IGNORECASE))) if _phone_prefix else None
            filters.append(lambda n: re.match(_phone_number, str(n['phone_number'], re.IGNORECASE))) if _phone_number else None
            filters.append(lambda n: re.match(_street_number, str(n['street_number'], re.IGNORECASE))) if _street_number else None
            filters.append(lambda n: re.match(_street_name, n['street_name'], re.IGNORECASE)) if _street_name else None
            filters.append(lambda n: re.match(_city, n['city'], re.IGNORECASE)) if _city else None
            filters.append(lambda n: re.match(_description, n['description'], re.IGNORECASE)) if _description else None
            return filters

        parser = reqparse.RequestParser()
        _id = argument_add('id', parser)
        _date = argument_add('date', parser)
        _after = argument_add('after', parser)
        if _after:
            try:
                _after = parse_time(_after)
                datetime.strptime(_after, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                _after = None
        _before = argument_add('before', parser)
        if _before:
            try:
                _before = parse_time(_before)
                datetime.strptime(_before, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                _before = None
        _name = argument_add('name', parser)
        _last_name = argument_add('last_name', parser)
        _phone_prefix = argument_add('phone_prefix', parser)
        _phone_number = argument_add('phone_number', parser)
        _street_number = argument_add('street_number', parser)
        _street_name = argument_add('street_name', parser)
        _city = argument_add('city', parser)
        _description = argument_add('description', parser)

        items_list = integrate_items()
        filters = define_filters()
        filtered_list = filter(lambda x: all(f(x) for f in filters), items_list['items'])
        return filtered_list        


@api.resource('/notification/id/<string:url_id>')
class NotificationID(Resource):
    def get(self, url_id):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_id, x['id'], re.IGNORECASE)]


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
            date_formatted = parse_time(url_date)
            datetime.strptime(date_formatted, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, IndexError):
            return {'error': 'Invalid data format. Use %Y-%m-%dT%H:%M:%S',
                'hint': 'It is allowed to provide incomplete data (%Y, %Y-%m, etc)'}

        if operator == '>':
            return [x for x in integrate_items()['items'] if x['date'] > date_formatted]
        elif operator == '<':
            return [x for x in integrate_items()['items'] if x['date'] < date_formatted]
        if operator == '=':
            return [x for x in integrate_items()['items'] if x['date'] == date_formatted]


@api.resource('/notification/street/<string:url_street>')
class NotificationSTREET(Resource):
    def get(self, url_street):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_street, x['street_name'], re.IGNORECASE)]


@api.resource('/notification/city/<string:url_city>')
class NotificationCITY(Resource):
    def get(self, url_city):
        return [
            x 
            for x in integrate_items()['items'] 
            if re.match(url_city, x['city'], re.IGNORECASE)]


@api.resource('/notification/description/<string:url_description>')
class NotificationDESCRIPTION(Resource):
    def get(self, url_description):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_description, x['description'], re.IGNORECASE)]


@api.resource('/caller/name/<string:url_name>')
class CallerNAME(Resource):
    def get(self, url_name):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_name, x['name'], re.IGNORECASE)]


@api.resource('/caller/last_name/<string:url_last_name>')
class CallerLASTNAME(Resource):
    def get(self, url_last_name):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_last_name, x['last_name'], re.IGNORECASE)]


@api.resource('/caller/phone_prefix/<string:url_phone_prefix>')
class CallerPHONEPREFIX(Resource):
    def get(self, url_phone_prefix):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_phone_prefix, str(x['phone_prefix'], re.IGNORECASE))]


@api.resource('/caller/phone_number/<string:url_phone_number>')
class CallerPHONENUMBER(Resource):
    def get(self, url_phone_number):
        return [
            x 
            for x in integrate_items()['items']
            if re.match(url_phone_number, str(x['phone_number'], re.IGNORECASE))]

 
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

def parse_time(date):
    datetime_list = re.findall('\d+', date)

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


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3333)
