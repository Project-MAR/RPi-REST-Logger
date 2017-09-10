#!/usr/bin/python3
from datetime import datetime
import time, random
import psycopg2

conn = psycopg2.connect(
    database="sensordb",
    user="postgres",
    password="raspDB",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Find  last ID
cur.execute("SELECT * FROM sensortable ORDER BY ID DESC LIMIT 1") # SELECT Last record
conn.commit()
result = cur.fetchall()
conn.close()
lastID = result[0][0]

while(True):
    lastID += 1
    conn = psycopg2.connect(
        database="sensordb",
        user="postgres",
        password="raspDB",
        host="127.0.0.1",
        port="5432"
    )
    cur = conn.cursor()

    timestamp = str(datetime.now())
    timestamp = timestamp[0:19]
    sensorValue = random.randint(0, 100)/2

    query =  "INSERT INTO sensortable (ID, NAME, TYPE, VALUE, DATE) VALUES (%s, %s, %s, %s, %s);"
    data = (lastID, 'dummySensor0', 0, sensorValue, timestamp);
    cur.execute(query, data)
    conn.commit()
    conn.close()
    print("Save record: " + str(lastID))
    time.sleep(3600)    # Delay, second
