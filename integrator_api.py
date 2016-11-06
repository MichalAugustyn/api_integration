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
        return integrate_items(req_1, req_2)


@api.resource('/notification/id/<string:url_id>')
class NotificationID(Resource):
    def get(self, url_id):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['id'])]


@api.resource('/notification/date/<string:url_date>')
class NotificationDATE(Resource):
    def get(self, url_date):
        # datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S')
        pass


@api.resource('/notification/street/<string:url_street>')
class NotificationSTREET(Resource):
    def get(self, url_street):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['street_name'])]


@api.resource('/notification/city/<string:url_city>')
class NotificationCITY(Resource):
    def get(self, url_city):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['city'])]


@api.resource('/notification/description/<string:url_description>')
class NotificationDESCRIPTION(Resource):
    def get(self, url_description):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['description'])]


@api.resource('/caller/name/<string:url_name>')
class CallerNAME(Resource):
    def get(self, url_name):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['name'])]


@api.resource('/caller/name/<string:url_name>')
class CallerLASTNAME(Resource):
    def get(self, url_name):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['last_name'])]


@api.resource('/caller/phone_prefix/<string:url_phone_prefix>')
class CallerPHONEPREFIX(Resource):
    def get(self, url_phone_prefix):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['phone_prefix'])]


@api.resource('/caller/phone_number/<string:url_phone_number>')
class CallerPHONENUMBER(Resource):
    def get(self, url_phone_number):
        return [
            x 
            for x in integrate_items(req_1, req_2) 
            if re.match(url_id, x['phone_number'])]

 
def integrate_items(provider_1_request, provider_2_request):
        provider_1_request = requests.get('http://localhost:1111/notification')
        provider_2_request = requests.get('http://localhost:2222/notification')
        provider_1_items = loads(json.loads(provider_1_request.text))['response']
        provider_1_integrated = [{
            'id': x['id'],
            'date': x['date_time'],
            'name': x['name'],
            'last_name': x['last_name'],
            'phone_prefix': int(re.findall('\((\d+)\)', x['phone'])[0]),
            'phone_number': int("".join(re.findall('(\d+)-(\d+)', x['phone'])[0])),
            'street_number': int(re.findall('(\d+) (.+)', x['address'])[0][0]),
            'street_name': re.findall('(\d+) (.+)', x['address'])[0][1],
            'city': x['city'],
            'description': x['additional_information']
            } for x in provider_1_items['items'] ]

        provider_2_items = json.loads(provider_2_request.text)
        provider_2_integrated = [{
            'id': x['id'],
            'date': x['date'],
            'name': x['name'].split()[0],
            'last_name': x['name'].split()[1],
            'phone_prefix': x['phone_prefix'],
            'phone_number': x['phone_number'],
            'street_number': x['street_number'],
            'street_name': x['street_name'],
            'city': x['city'],
            'description': x['description']
            } for x in provider_2_items['items']]

        return sorted(provider_2_integrated + provider_1_integrated,
            key=lambda x: x['date'])

if __name__ == '__main__':
    app.run(debug=True)
