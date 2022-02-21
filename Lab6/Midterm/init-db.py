import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Lab6;")
cursor.execute("USE Lab6")
cursor.execute("DROP TABLE IF EXISTS DHT11;")
cursor.execute("DROP TABLE IF EXISTS Photoresistor;")

try:
    cursor.execute("""
    CREATE TABLE DHT11 (
        id          integer  AUTO_INCREMENT PRIMARY KEY,
        Temperature VARCHAR(50) NOT NULL,
        Humidity    VARCHAR(50) NOT NULL 
    );
    """)

    query = "INSERT INTO DHT11 (Temperature, Humidity) VALUES (%s, %s)"
    values = [
        ('72.00','65.00')
    ]
    cursor.executemany(query, values)

    cursor.execute("""
    CREATE TABLE Photoresistor (
        id          integer  AUTO_INCREMENT PRIMARY KEY,
        Light       integer  NOT NULL 
    );
    """)

    cursor.execute("INSERT INTO Photoresistor (Light) VALUES (%d);" % 100)
    db.commit()

except RuntimeError as err:
    print("runtime error: {0}".format(err))

