'''
    First create a db in postgres named locinfo.
'''
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import psycopg2

hostname = 'localhost'
username = 'postgres'
database = 'locinfo'
password = 'YOUR_POSTGRES_PASSWORD'

''' part of Task 1'''
print("Setting up geo_info table....")

# Loading CSV in a dataframe
df=pd.read_csv("IN.csv", delimiter=',')
#print(df.head())

# storing df in sql using pandas
engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(username,password,hostname,database))
df.to_sql('geo_info', engine)

'''
        TASK 3 LOAD JSON IN THE TABLE
'''
myConnection = psycopg2.connect( host=hostname, password=password, user=username, dbname=database )
cur = myConnection.cursor()
query = "CREATE EXTENSION IF NOT EXISTS earthdistance"
cur.execute(query)

print("Setting up geo_cords table....")
geojs = pd.read_json("map.geojson")
features = geojs["features"]
name = []
parent = []
coor = []
for row in features:
    name.append(row["properties"]["name"])
    parent.append(row["properties"]["parent"])
for lis in features:
    coor.append(lis['geometry']["coordinates"][0])

geojs = pd.DataFrame(name,columns=["name"])
geojs["parent"] = parent
geojs["coordinates"]=coor

geojs.to_sql('geo_cords', engine)

print("Database Configured!")
