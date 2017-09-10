 #!/usr/bin/python3
import psycopg2

conn = psycopg2.connect(
    database="sensordb",
    user="postgres",
    password="raspDB",
    host="127.0.0.1",
    port="5432"
)

cur = conn.cursor()
cur.execute("SELECT * FROM sensortable")
rows = cur.fetchall()
conn.close()

for row in rows:
    resultDict = {
        "ID"    : row[0],
        "NAME"  : row[1],
        "TYPE"  : row[2],
        "VALUE" : row[3],
        "DATE"  : str(row[4])
    }
    print(resultDict)
