from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import numpy as np
import cv2
# import serial               #import serial package
# from time import sleep
# import webbrowser           #import package for opening link in browser
# import sys                  #import system package
# import RPi.GPIO as GPIO
# from RpiMotorLib import RpiMotorLib
# import time
import datetime



# load_dotenv('credentials.env')
# db_host = os.environ['MYSQL_HOST']
# db_user = os.environ['MYSQL_USER']
# db_pass = os.environ['MYSQL_PASSWORD']
# db_name = os.environ['MYSQL_DATABASE']

# db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
# cursor = db.cursor()

def index_page(req):
    return FileResponse('index.html')

def get_object(req):
    object_id = int(req.matchdict['object_id'])
    
    print('Object_id:', str(object_id))

    response = {
        'error':            '',
        'GPS_coord':        'test coordinate'
    }
    return response

def store_location(req):
    object_id = int(req.matchdict['object_id'])
    
    print('Object_id:', str(object_id))

    response = {
        'store_msg': 'Object location is successfully stored into database!'
    }
    return response

if __name__ == "__main__":
    with Configurator() as config:
        # create a route for home
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')
        
        # create a route for objects
        config.add_route('objects', '/objects/{object_id}')
        config.add_view(get_object, route_name='objects', renderer='json')

        # create a route for storing objects
        config.add_route('store_loc', '/store_loc/{object_id}')
        config.add_view(store_location, route_name='store_loc', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)  
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()