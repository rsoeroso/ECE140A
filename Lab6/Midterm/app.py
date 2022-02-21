from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
from ADCDevice import *

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Empty tables before starting
cursor.execute("TRUNCATE Photoresistor")
cursor.execute("TRUNCATE DHT11")

DHTPin = 16         # define DHTPin
# Defines the data bit that is transmitted preferentially in the shiftOut function.
LSBFIRST = 1
MSBFIRST = 2
# define the pins for 74HC595
dataPin   = 11      # DS Pin of 74HC595(Pin14)
latchPin  = 13      # ST_CP Pin of 74HC595(Pin12)
clockPin = 15       # CH_CP Pin of 74HC595(Pin11)

GPIO.setmode(GPIO.BOARD)    # use PHYSICAL GPIO Numbering
GPIO.setup(dataPin, GPIO.OUT) # set pin to OUTPUT mode
GPIO.setup(latchPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)

global adc
adc = ADCDevice()   # Define an ADCDevice class object
if(adc.detectI2C(0x4b)): # Detect the ads7830
    adc = ADS7830()
else:
    print("No correct I2C address found, \n"
    "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
    "Program Exit. \n");
    exit(-1)


def get_home(req):
    return FileResponse('index.html')

def get_everything(req):
    sensor_id = int(req.matchdict['sensor_id'])
    average_id = int(req.matchdict['average_id'])
    LED_id = int(req.matchdict['LED_id'])

    # DEBUG
    # print('sensor_id %s' % sensor_id)
    # print('average_id %s' % average_id)
    # print('LED_id %s' % LED_id)
    
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
    
    # Handle sensors for immediate reading:

    # Read both the Photoresistor and the DHT11
    if (sensor_id == 1 and average_id == 1):
        cursor.execute("TRUNCATE Photoresistor")
        cursor.execute("TRUNCATE DHT11")

        cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())

        query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
        values = [
        (getTemperature() * (9/5) + 32, getHumidity())
        ]
        cursor.executemany(query, values)
        db.commit()

        cursor.execute("SELECT Light FROM Photoresistor;") 
        theLight = cursor.fetchone()
        cursor.execute("SELECT Temperature FROM DHT11;") 
        theTemp = cursor.fetchone()
        cursor.execute("SELECT Humidity FROM DHT11;") 
        theHumidity = cursor.fetchone()

        response = {
        'error': '',
        'light_avg': '%d' % (theLight[0]),
        'temp_avg': ' %s' % ((theTemp[0])[0:2]),
        'humid_avg': ' %s' % (theHumidity[0])
    }

    # Only read the Photoresistor
    if (sensor_id == 2 and average_id == 1):
        cursor.execute("TRUNCATE Photoresistor")

        cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())
        db.commit()

        cursor.execute("SELECT Light FROM Photoresistor;") 
        theLight = cursor.fetchone()

        response = {
        'error': '',
        'light_avg': '%d' % (theLight),
        'temp_avg': 'N/A',
        'humid_avg': 'N/A'
    }

    # Only read the DHT11
    if (sensor_id == 3 and average_id == 1):
        cursor.execute("TRUNCATE DHT11")

        query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
        values = [
        (getTemperature() * (9/5) + 32, getHumidity())
        ]
        cursor.executemany(query, values)
        db.commit()

        cursor.execute("SELECT Temperature FROM DHT11;") 
        theTemp = cursor.fetchone()
        cursor.execute("SELECT Humidity FROM DHT11;") 
        theHumidity = cursor.fetchone()

        response = {
        'error': '',
        'light_avg': 'N/A',
        'temp_avg': ' %s' % ((theTemp[0])[0:2]),
        'humid_avg': ' %s' % (theHumidity[0])
    }

    # Handle sensors for 1 min average

    # Read both the Photoresistor and the DHT11
    if (sensor_id == 1 and average_id == 2):
        cursor.execute("TRUNCATE Photoresistor")
        cursor.execute("TRUNCATE DHT11")
        count = 0
        lightAvg = 0
        tempAvg = 0
        humAvg = 0
        for count in range(22):
            cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())
            query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
            values = [
            (getTemperature() * (9/5) + 32, getHumidity())
            ]
            cursor.executemany(query, values)
            db.commit()
            time.sleep(1)
        cursor.execute("SELECT AVG(Light) AS lightAvg FROM Photoresistor;") 
        lightAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Temperature) AS tempAvg FROM DHT11;") 
        tempAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Humidity) AS humAvg FROM DHT11;")
        humAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': '%d' % lightAvg,
            'temp_avg': ' %s' % ((tempAvg[0])[0:2]),
            'humid_avg': ' %s' % (humAvg[0])     
    }

    # Only read the Photoresistor
    if (sensor_id == 2 and average_id == 2):
        cursor.execute("TRUNCATE Photoresistor")
        count = 0
        lightAvg = 0
        for count in range(60):
            cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())
            db.commit()
            print(count)
            time.sleep(1)
        cursor.execute("SELECT AVG(Light) AS lightAvg FROM Photoresistor;") 
        lightAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': '%d' % (lightAvg),
            'temp_avg': 'N/A',
            'humid_avg': 'N/A'  
    }

    # Only read the DHT11
    if (sensor_id == 3 and average_id == 2):
        cursor.execute("TRUNCATE DHT11")
        count = 0
        tempAvg = 0
        humAvg = 0
        for count in range(22):
            query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
            values = [
            (getTemperature() * (9/5) + 32, getHumidity())
            ]
            cursor.executemany(query, values)
            db.commit()
        cursor.execute("SELECT AVG(Temperature) AS tempAvg FROM DHT11;") 
        tempAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Humidity) AS humAvg FROM DHT11;")
        humAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': 'N/A',
            'temp_avg': ' %s' % (str(tempAvg[0])[0:2]),
            'humid_avg': ' %s' % (str(humAvg[0])[0:2])         
    }

    # Handle sensors for 5 min average

    # Read both the Photoresistor and the DHT11
    if (sensor_id == 1 and average_id == 3):
        cursor.execute("TRUNCATE Photoresistor")
        cursor.execute("TRUNCATE DHT11")
        count = 0
        lightAvg = 0
        tempAvg = 0
        humAvg = 0
        for count in range(110):
            cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())
            query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
            values = [
            (getTemperature() * (9/5) + 32, getHumidity())
            ]
            cursor.executemany(query, values)
            db.commit()
            time.sleep(1)
        cursor.execute("SELECT AVG(Light) AS lightAvg FROM Photoresistor;") 
        lightAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Temperature) AS tempAvg FROM DHT11;") 
        tempAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Humidity) AS humAvg FROM DHT11;")
        humAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': '%d' % lightAvg,
            'temp_avg': ' %s' % ((tempAvg[0])[0:2]),
            'humid_avg': ' %s' % (humAvg[0])     
    }

    # Only read the Photoresistor
    if (sensor_id == 2 and average_id == 3):
        cursor.execute("TRUNCATE Photoresistor")
        count = 0
        lightAvg = 0
        for count in range(300):
            cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % getLight())
            db.commit()
            time.sleep(1)
        cursor.execute("SELECT AVG(Light) AS lightAvg FROM Photoresistor;") 
        lightAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': '%d' % lightAvg,
            'temp_avg': 'N/A',
            'humid_avg': 'N/A'  
    }

    # Only read the DHT11
    if (sensor_id == 3 and average_id == 3):
        cursor.execute("TRUNCATE DHT11")
        count = 0
        tempAvg = 0
        humAvg = 0
        for count in range(110):
            query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
            values = [
            (getTemperature() * (9/5) + 32, getHumidity())
            ]
            cursor.executemany(query, values)
            db.commit()
            time.sleep(1)
        cursor.execute("SELECT AVG(Temperature) AS tempAvg FROM DHT11;") 
        tempAvg = cursor.fetchone()
        cursor.execute("SELECT AVG(Humidity) AS humAvg FROM DHT11;")
        humAvg = cursor.fetchone()

        response = {
            'error': '',
            'light_avg': 'N/A',
            'temp_avg': ' %s' % ((tempAvg[0])[0:2]),
            'humid_avg': ' %s' % (humAvg[0])         
    }

    # Handle LED

    if (LED_id == 1):
        
        x=0x01
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)  # Output low level to latchPin
            shiftOut(dataPin,clockPin,LSBFIRST,x) # Send serial data to 74HC595
            GPIO.output(latchPin,GPIO.HIGH) # Output high level to latchPin, and 74HC595 will update the data to the parallel output port.
            x<<=1 # make the variable move one bit to left once, then the bright LED move one step to the left once.
            time.sleep(0.1)
        x=0x80
        for i in range(0,8):
            GPIO.output(latchPin,GPIO.LOW)
            shiftOut(dataPin,clockPin,LSBFIRST,x)
            GPIO.output(latchPin,GPIO.HIGH)
            x>>=1
            time.sleep(0.1)
        return

    
    return response

def setup():
    GPIO.setmode(GPIO.BOARD)     
    # GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(DHTPin, GPIO.IN)    # set echoPin to INPUT mode

def getTemperature():
    dht = DHT.DHT(DHTPin)
    dht.readDHT11() #read DHT11 and get a return value.
    theTemp = dht.temperature
    return theTemp

def getHumidity():
    dht = DHT.DHT(DHTPin)
    dht.readDHT11() #read DHT11 and get a return value.
    theHumidity = dht.humidity
    return theHumidity

def getLight():
    value = adc.analogRead(0)    # read the ADC value of channel 0
    return value

def shiftOut(dPin,cPin,order,val):
        for i in range(0,8):
            GPIO.output(cPin,GPIO.LOW);
            if(order == LSBFIRST):
                GPIO.output(dPin,(0x01&(val>>i)==0x01) and GPIO.HIGH or GPIO.LOW)
            elif(order == MSBFIRST):
                GPIO.output(dPin,(0x80&(val<<i)==0x80) and GPIO.HIGH or GPIO.LOW)
            GPIO.output(cPin,GPIO.HIGH);

def destroy():
    adc.close()
    GPIO.cleanup()


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