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

cursor.execute("CREATE DATABASE IF NOT EXISTS Lab8;")
cursor.execute("USE Lab8")
cursor.execute("DROP TABLE IF EXISTS found_objects;")
cursor.execute("DROP TABLE IF EXISTS objects;")

try:

    cursor.execute("""
    CREATE TABLE objects (
        id                  integer  AUTO_INCREMENT PRIMARY KEY,
        object_name         VARCHAR(50) NOT NULL,
        HSV_1               VARCHAR(50) NOT NULL,
        HSV_2               VARCHAR(50) NOT NULL,
        HSV_3               VARCHAR(50) NOT NULL,
        HSV_4               VARCHAR(50) NOT NULL
    );
    """)

    query = "INSERT INTO objects (object_name, HSV_1, HSV_2, HSV_3, HSV_4) VALUES (%s, %s, %s, %s, %s)"
    values = [
        ('Red Box', '0', '10', '160', '179'),
        ('Blue Album', '90', '130', '130', '140'),
        ('Green Folder', '40','60', '60', '80')
    ]
    cursor.executemany(query, values)

    cursor.execute("""
    CREATE TABLE found_objects (
        id                  integer,
        object_name         VARCHAR(50) NULL,
        coordinates         VARCHAR(50) NULL,
        address             VARCHAR(100) NULL,
        created_at          TIMESTAMP
    );
    """)
    
    db.commit()

except RuntimeError as err:
    print("runtime error: {0}".format(err))

