from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os

# load_dotenv('credentials.env')
# db_host = os.environ['MYSQL_HOST']
# db_user = os.environ['MYSQL_USER']
# db_pass = os.environ['MYSQL_PASSWORD']
# db_name = os.environ['MYSQL_DATABASE']

def get_home(req):
    return FileResponse('index.html')

def get_everything(req):
    sensor_id = int(req.matchdict['sensor_id'])
    average_id = int(req.matchdict['average_id'])
    LED_id = int(req.matchdict['LED_id'])

    # DEBUG
    print('sensor_id %s' % sensor_id)
    print('average_id %s' % average_id)
    print('LED_id %s' % LED_id)
    
    '''
    sensor_id
    0 -> LED button is pressed, don't change the average value display
    1 -> Display Photoresistor and DHT-11 value
    2 -> Display Photoresistor only
    3 -> Display DHT-11 only
    
    average_id
    0 -> LED button is pressed, don't change the average value display
    1 -> Display the latest value
    2 -> Display the average value in 1 minute
    3 -> Display the average value in 5 minutes

    LED_id
    0 -> LED off
    1 -> LED on
    2 -> no change
    '''

    response = {
        'error': '',
        'light_avg': 750,
        'temp_avg': 20,
        'humid_avg': 20
    }

    return response
    
if __name__ == "__main__":
    with Configurator() as config:
        # add route for home
        config.add_route('home', '/')
        config.add_view(get_home, route_name='home', renderer='json')

        # add route for web functionalities
        config.add_route('get_everything', '/{sensor_id}/{average_id}/{LED_id}')
        config.add_view(get_everything, route_name='get_everything', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)        

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)  
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()
