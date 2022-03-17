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

try:
    cursor.execute("""
    CREATE TABLE found_objects (
        id                  integer  AUTO_INCREMENT PRIMARY KEY,
        object_name         VARCHAR(50) NOT NULL,
        address             VARCHAR(50) NOT NULL,
        created_at          TIMESTAMP
    );
    """)

    # query = "INSERT INTO Plates (Name, Plate, created_at) VALUES (%s, %s, %s)"
    # values = [
    #     ('Don', '1FYT860', datetime.datetime.now())
    # ]
    # cursor.executemany(query, values)
    db.commit()

except RuntimeError as err:
    print("runtime error: {0}".format(err))

