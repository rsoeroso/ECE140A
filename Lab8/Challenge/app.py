from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import numpy as np
import cv2
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
import datetime
import serial               #import serial package
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package
import reverse_geocode

# global location_list
global NMEA_buff
global lat_in_degrees
global long_in_degrees

location_list = (0, 0)

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

cursor.execute("TRUNCATE found_objects")

def find_object(HSV1, HSV2, HSV3, HSV4):
    #video capture likely to be 0 or 1
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    #Stepper Motor Setup
    GpioPins = [18, 23, 24, 25]

    # Declare a named instance of class pass a name and motor type
    mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
    #min time between motor steps (ie max speed)
    step_time = .002

    #PID Gain Values
    Kp = 0.001
    Kd = 0.0001
    Ki = 0.0001

    #error values
    d_error = 0
    last_error = 0
    sum_error = 0

    count = 0
    speedcount = 0
    switch = 1

    while(1):

        # print(HSV1)
        _,frame=cap.read()

        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #red is on upper and lower of the hsv scale. Requires 2 ranges 
        lower1 = np.array([int(HSV1[0]), 50, 20])
        upper1 = np.array([int(HSV2[0]), 255, 255])
        lower2 = np.array([int(HSV3[0]), 50, 20])
        upper2 = np.array([int(HSV4[0]), 255, 255])
        
        #masks input image with upper and lower red ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        color_only2 = cv2.inRange(hsv, lower2 , upper2)
        
        color_only = color_only1 + color_only2
        
        mask=np.ones((5,5),np.uint8)
        
        
        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(color_only,cv2.MORPH_OPEN,mask)
        cv2.imwrite('Masked image.png', opening)

        #run connected components algo to return all objects it sees.        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 1:
            print('Object Found')
            start = time.time()
            #extracts the label of the largest none background component and displays distance from center and image.
            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            Obj = b == max_label
            Obj = np.uint8(Obj)
            Obj[Obj > 0] = 255
            cv2.imwrite(f"./Frames/data_{Obj}.png", Obj)
            
            #calculate error from center column of masked image
            error = -1 * (320 - centroids[max_label][0])

    #speed gain calculated from PID gain values
            speed = Kp * error + Ki * sum_error + Kd * d_error
            # print(speed)
            
            #if negative speed change direction
            if speed < 0:
                direction = False
            else:
                direction = True
            
            #inverse speed set for multiplying step time (lower step time = faster speed)
            speed_inv = abs(1/(speed))
            
            #get delta time between loops
            delta_t = time.time() - start
            #calculate derivative error
            d_error = (error - last_error)/delta_t
            #integrated error
            sum_error += (error * delta_t)
            last_error = error
            
            #buffer of 20 only runs within 20
            if abs(error) > 30:
                mymotortest.motor_run(GpioPins , speed_inv * step_time, 1, direction, False, "full", .05)
            else:
                #run 0 steps if within an error of 20
                mymotortest.motor_run(GpioPins , step_time, 0, direction, False, "full", .05)
                count = count + 1
        
        else:
            # print('no object in view')
            
            speed = 0.2
            speed_inv = abs(1/(speed))

            #if negative speed change direction
            if switch < 0:
                direction = False 
            else:
                direction = True
            
            mymotortest.motor_run(GpioPins , 0.002, 3, direction, False, "full", .05)

            if (speedcount % 20 == 1):
                switch = switch * -1
            
            speedcount = speedcount + 1
            print('No object in view')
            
        if count == 10:
            break


#convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
   decimal_value = raw_value/100.00
   degrees = int(decimal_value)
   mm_mmmm = (decimal_value - int(decimal_value))/0.6
   position = degrees + mm_mmmm
   position = "%.4f" %(position)
   return float(position)

def find_location():
    gpswait = 0
    gpgga_info = "$GPGGA,"
    ser = serial.Serial ("/dev/serial0")              #Open port with baud rate
    GPGGA_buffer = 0
    NMEA_buff = 0
    lat_in_degrees = 0
    long_in_degrees = 0
    
    while gpswait < 1:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer

            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_latitude_dir = NMEA_buff[2]            #extract the direction of latitude(N/S)
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            nmea_longitude_dir = NMEA_buff[2]           #extract the direction of longitude(E/W)

            print("NMEA Time: ", nmea_time,'\n')
            print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')

            lat = float(nmea_latitude)                  #convert string into float for calculation
            longi = float(nmea_longitude)               #convert string into float for calculation


            #get latitude in degree decimal format with direction
            lat_in_degrees = convert_to_degrees(lat) if nmea_latitude_dir == 'N' else (-1 * convert_to_degrees(lat))  
            #get longitude in degree decimal format with direction
            long_in_degrees = convert_to_degrees(longi) if nmea_longitude_dir == 'E' else (-1 * convert_to_degrees(longi))

            print("lat in degrees:", str(lat_in_degrees)," long in degree: ", str(long_in_degrees), '\n')
            map_link = 'http://maps.google.com/?q=' + str(lat_in_degrees) + ',' + str(long_in_degrees)    #create link to plot location on Google map
            coordinates = (lat_in_degrees, long_in_degrees), (0, 0)
            city = reverse_geocode.search(coordinates)[0]
            theCity = str(city["city"]) + ", " + str(city["country"])
            address = (str(lat_in_degrees), str(long_in_degrees))
            print(theCity)
            print(map_link)               #press ctrl+c to plot on map and exit
            print("------------------------------------------------------------\n")
            gpswait = gpswait + 1

    return address, theCity

def index_page(req):
    return FileResponse('index.html')

def get_object(req):
    object_id = int(req.matchdict['object_id'])
    print('Object_id:', str(object_id))
    
    # Find object function, returns coordinates
    # cursor.execute("SELECT * FROM objects WHERE id = %s;", object_id)
    cursor.execute("SELECT object_name FROM objects WHERE id = %d;" % object_id)
    obj_name = cursor.fetchone() 
    cursor.execute("SELECT HSV_1 FROM objects WHERE id = %d;" % object_id)
    hsv1 = cursor.fetchone()
    cursor.execute("SELECT HSV_2 FROM objects WHERE id = %d;" % object_id) 
    hsv2 = cursor.fetchone()
    cursor.execute("SELECT HSV_3 FROM objects WHERE id = %d;" % object_id) 
    hsv3 = cursor.fetchone()
    cursor.execute("SELECT HSV_4 FROM objects WHERE id = %d;" % object_id) 
    hsv4 = cursor.fetchone()

    find_object(hsv1, hsv2, hsv3, hsv4) 
    coordinates, city = find_location()
    # print(coordinates[0])
    # print(coordinates[1])
    global location_list
    location_list = (coordinates, city)
    # print(location_list)

    response = {
        'name':         ' %s' % (obj_name[0]),
        'coordinates':  ' %s, %s' % (coordinates[0], coordinates[1]),
        'address':      ' %s' % (city)
    }
    return response

def store_location(req):
    object_id = int(req.matchdict['object_id']) 
    print('Object_id:', str(object_id))
    print(location_list)

    cursor.execute("SELECT object_name FROM objects WHERE id = %d;" % object_id)
    obj_name = cursor.fetchone()
    obj_name = obj_name[0]
    # print(obj_name)
    cursor.execute("SELECT object_name FROM found_objects WHERE object_name = '%s';" % str(obj_name))
    null_obj = cursor.fetchone()
    # print(null_obj)
    
    # cursor.execute("SELECT object_name FROM found_objects WHERE id = %d;" % object_id)
    # obj_name = cursor.fetchone()
    # found_obj_name = obj_name + 
    if null_obj == None:

        query = "INSERT INTO found_objects (id, object_name, coordinates, address) VALUES (%s, %s, %s, %s)"
        values = [
            (str(object_id), str(obj_name), str(location_list[0]), str(location_list[1]))
        ]
        cursor.executemany(query, values)

        # print(obj_name)

    else:

        cursor.execute("SELECT count(*) from found_objects WHERE id = %s GROUP BY id;" % str(object_id))
        append = cursor.fetchone()
        obj_name += str(append[0] + 1)

        # print(obj_name)

        query = "INSERT INTO found_objects (id, object_name, coordinates, address) VALUES (%s, %s, %s, %s)"
        values = [
            (str(object_id), str(obj_name), str(location_list[0]), str(location_list[1]))
        ]
        cursor.executemany(query, values)

    db.commit()

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