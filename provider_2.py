#!/usr/bin/python
import re
import mysql.connector
import MySQLdb
import time
filepath = './LA_logs'
database_name = 'provider_2'
connect = MySQLdb.connect('localhost', 'root', 'root', database_name)
with connect:
    cursor = connect.cursor()
    cursor._defer_warnings = True
    cursor.execute('DROP TABLE IF EXISTS caller')
    cursor.execute('''CREATE TABLE caller(\
    id varchar(6) PRIMARY KEY, \
    name varchar(30) NOT NULL, \
    phone_prefix int(3), \
    phone_number int(7) NOT NULL);''')
    print "[+] Created table caller"
    cursor.execute('DROP TABLE IF EXISTS notification')
    cursor.execute('''CREATE TABLE notification(\
    id varchar(6) PRIMARY KEY, \
    date datetime NOT NULL, \
    street_number int(5) NOT NULL, \
    street_name varchar(30) NOT NULL, \
    city varchar(30) NOT NULL, \
    caller_id varchar(6), \
    description varchar(300) NOT NULL);''')
    print "[+] Created table notification"
    i = 0
    prefix = 'LA'
    for line in open(filepath, 'r'):
        list = re.findall(
            '\[(.+)\] (.+) (\d+), (.+) - ([\w\ ]+) (\d+) (\d+) \[(.+)\]', line.strip())[0]
        date = time.strptime(list[0], "%d-%m-%Y %H:%M:%S")
        date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        cursor.execute('''INSERT INTO caller VALUES(\"%s\", \"%s\", %d, %d)''' % (
            "%sC%03d" % (prefix, i), list[4], int(list[5]), int(list[6])))
        cursor.execute('''INSERT INTO notification VALUES(\"%s\", \"%s\", %d, \"%s\", \"%s\", \"%s\", \"%s\")''' % (
            "%sN%03d" % (prefix, i), date, int(list[2]), list[1], list[3], "%sC%03d" % (prefix, i), list[7]))
        i += 1
    else:
        print "[+] Added %d rows to columns: caller, notification" % i
