from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# JSON which maps plates to ID
plate_photos = [
    {"id":1, "img": "Arizona_47.jpg"},
    {"id":2, "img": "Contrast.jpg"},
    {"id":3, "img": "Delaware_Plate.png"}
]

def index_page(req):
    return FileResponse('index.html')

def get_plate(req):
    idx = int(req.matchdict['plate_id'])-1

    response = {
        'error':            '',
        'image':            plate_photos[idx]['img'],
        'text_detected':    'ABCDEFG'
    }

    return response

if __name__ == "__main__":
    with Configurator() as config:
        # create a route for home
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')
        
        # create a route for plates
        config.add_route('plates', '/plates/{plate_id}')
        config.add_view(get_plate, route_name='plates', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)  
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()

