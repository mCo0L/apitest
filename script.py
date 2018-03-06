from flask import Flask, request, json
from math import radians, atan2, sin, cos, sqrt
import pandas as pd
import psycopg2
from shapely.geometry import MultiPoint,Point, Polygon

hostname = 'localhost'
username = 'postgres'
database = 'locinfo'
password = 'YOUR_POSTGRES_PASSWORD'
myConnection = psycopg2.connect( host=hostname, password=password, user=username, dbname=database )

app = Flask(__name__)

@app.route('/post_location', methods=['POST'])
def post_location():
    if request.headers['Content-Type'] == 'text/plain':
        try:
            text=request.data.decode("utf-8")
            lat,lon,pin,place,ad=text.split("+")
            cur=myConnection.cursor()

            ''' TO CHECK IF PINCODE ALREADY PRESENT IN DATABASE'''

            cur.execute("SELECT key FROM geo_info WHERE key = {} ".format("\'"+pin+"\'"))
            if cur.rowcount>0:
                return "Location already present in DataBase"
            else:

                """
                After checking the condition of pincode.
                CHECKING IF A NEARBY LOCATION IS PRESENT IN DATABASE

                This condition checks if a location in radius of almost 2.2km is present.
                """

                query = "SELECT latitude, longitude FROM geo_info \
                WHERE (latitude >= {}-0.02 AND latitude <= {}+0.02) \
                AND (longitude >= {}-0.02 AND longitude <= {}+0.02) \
                ".format(float(lat), float(lat), float(lon), float(lon))
                cur.execute(query)
                if cur.rowcount>0:
                    print(cur.fetchall())
                    return "A Nearby/Same Location already present in DataBase"

                else:
                    cur.execute("INSERT INTO geo_info (admin_name1,latitude,longitude,key,place_name) VALUES (%s, %s, %s, %s, %s)",(ad,lat,lon,pin,place))
                    myConnection.commit()

                    lis = str(request.data)[2:-1].split('+')
                    return "---Location added--- \nLatitude: {} \nlongitude: {} \nPincode: {} \nPlace: {} \nState: {}".format(*lis)
        except:
            print("Invalid input provided!")
            return "Invalid Input!"


@app.route('/get_using_postgres',methods=['GET'])
def get_using_postgres():
    if request.headers['Content-Type'] == 'text/plain':
        try:
            text=request.data.decode("utf-8")
            lat,lon=text.split("+")

            cur=myConnection.cursor()
            query="SELECT geo_info.place_name FROM geo_info \
            WHERE earth_box(ll_to_earth({},{}),5000) @> ll_to_earth(geo_info.latitude, geo_info.longitude)".format(float(lat),float(lon))
            cur.execute(query)

            lis=[]
            if cur.rowcount == 0:
                return "No Place found in 5km Area!"
            for a in cur.fetchall():
                lis.append(str(a)[2:-3])
            return "Places in 5KM Radius:\n" + "\n".join(lis)
        except:
            print("Invalid input provided!")
            return "Invalid Input!"

@app.route('/get_using_self', methods=['GET','POST'])
def get_using_self():
    if request.headers['Content-Type'] == 'text/plain':
        try:
            text = request.data.decode("utf-8")
            lat1,lon1 = text.split("+")
            cur=myConnection.cursor()
            query="SELECT place_name,latitude,longitude FROM geo_info"
            cur.execute(query)
            if cur.rowcount == 0:
                return "No Place found in 5km Area!"
            else:
                lis=[]
                for place,lat2,lon2 in cur.fetchall():
                    if (lat2 is None) or (lon2 is None):
                        continue
                    distance = getDistanceFromLatLonInKm(float(lat1), float(lon1), float(lat2), float(lon2))
                    if distance<=5000:
                        lis.append(place)
                return "Places in 5km radius of given point are: \n" + "\n".join(lis)
        except:
            print("Invalid input provided!")
            return "Invalid Input!"

def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
    R = 6371.0
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c * 1000 ;
    return d

@app.route('/get_city_name', methods=['GET','POST'])
def get_city_name():
    if request.headers['Content-Type'] == 'text/plain':
        try:
            text = request.data.decode("utf-8")
            lat, lon = text.split("+")
            cur = myConnection.cursor()
            query = "SELECT name, coordinates FROM geo_cords"
            cur.execute(query)
            count = 0
            point = Point(float(lat), float(lon))
            for place, coor in cur.fetchall():
                lats = []
                lons = []
                coor = coor.replace("{","").replace("}","").split(",")
                coor = list(map(float, coor))
                for index, val in enumerate(coor):
                    if index%2==0:
                        lats.append(val)
                    else:
                        lons.append(val)
                points = []
                for i in range(len(lats)):
                    points.append(Point(lons[i],lats[i]))
                hull = MultiPoint(points=points).convex_hull
                if hull.contains(point):
                    count += 0
                    return "Location found in: "+place
            if count == 0:
                return "Location not found!"
        except:
            print("Invalid input provided!")
            return "Invalid Input!"

if __name__ == '__main__':
  app.run(port=8000, debug=True)
