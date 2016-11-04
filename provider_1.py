#!/usr/bin/python
import re
import mysql.connector
import MySQLdb
import time
filepath = './NY_logs'
database_name = 'provider_1'
connect = MySQLdb.connect('localhost', 'root', 'root', database_name)
with connect:
    cursor = connect.cursor()
    cursor._defer_warnings = True
    cursor.execute('DROP TABLE IF EXISTS caller')
    cursor.execute('''CREATE TABLE caller(\
    id varchar(6) PRIMARY KEY, \
    name varchar(30) NOT NULL, \
    last_name varchar(30) NOT NULL, \
    phone varchar(18) NOT NULL);''')
    print "[+] Created table caller"
    cursor.execute('DROP TABLE IF EXISTS notification')
    cursor.execute('''CREATE TABLE notification(\
    id varchar(6) PRIMARY KEY, \
    date_time datetime NOT NULL, \
    address varchar(30) NOT NULL, \
    city varchar(30) NOT NULL, \
    caller_id varchar(6) NOT NULL, \
    additional_information varchar(300) NOT NULL);''')
    print "[+] Created table notification"
    i = 0
    prefix = 'NY'
    for line in open(filepath, 'r'):
        list = re.findall(
            '\[(.+)\] (.+) - ([A-Z]+) ([A-Z]+) - (.*), (.+) - \"(.*)\"', line.strip())[0]
        date = time.strptime(list[0], "%Y-%m-%dT%H:%M:%SZ")
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        cursor.execute('''INSERT INTO caller VALUES(\"%s\", \"%s\", \"%s\", \"%s\")''' % (
            "%sC%03d" % (prefix, i), list[2], list[3], list[1]))
        cursor.execute('''INSERT INTO notification VALUES(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")''' % (
            "%sN%03d" % (prefix, i), date, list[4], list[5], "%sC%03d" % (prefix, i), list[6]))

        i += 1
    else:
        print "[+] Added %d rows to columns: caller, notification" % i
