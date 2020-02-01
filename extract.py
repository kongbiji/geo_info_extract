import sys
import requests
from PIL import Image
from PIL.ExifTags import TAGS

def gps_modify(old_lat, old_lon): #unfinished function
    print("[+] Modify GPS information")
    lat = input(">>latitude : ")
    lon = input(">>longitude: ")

def get_google_map_info(latit, longi, eleva):
    URL = 'https://maps.googleapis.com/maps/api/elevation/json?locations=' + str(latit) + ',' + str(longi) + '&key=[Google Map API Key value]'
    response = requests.get(URL)
    data = response.json()

    lat = data['results'][0]['location']['lat']
    lng = data['results'][0]['location']['lng']
    ele = data['results'][0]['elevation']

    if (eleva < ele-30) | (eleva > ele+30):
        print('[-] Possible GPS was manipulated ! ! !')

def get_exif(img_file):
    img = Image.open(img_file)
    exif = {}
    try:
        info = img._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value

        # Extract GPS informations
        gps = exif['GPSInfo']
        lat = gps[2]
        lon = gps[4]
        sea = gps[6]
        print(lat)
        print(lon)
        print(sea)

        # Calculate the latitude and longitude
        latDeg = lat[0][0] / float(lat[0][1])
        latMin = lat[1][0] / float(lat[1][1])
        latSec = lat[2][0] / float(lat[2][1])
        lonDeg = lon[0][0] / float(lon[0][1])
        lonMin = lon[1][0] / float(lon[1][1])
        lonSec = lon[2][0] / float(lon[2][1])
        sea_level = sea[0] / float(sea[1])

        latitude = (latDeg + (latMin + latSec / 60.0) / 60.0)
        if gps[1] == 'S': 
            latitude = latitude * -1
        longitude = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
        if gps[3] == 'W': 
            longitude = longitude * -1

        msg = '[+] Extract success\n>> latitude: ' + str(latitude) + '\n>> longitude: ' + str(longitude) + '\n>> sea level: ' + str(sea_level) + 'm'
        get_google_map_info(latitude, longitude, sea_level)
        return msg
    except: 
        msg = '[-] No GPS information'
        return msg

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extract.py example.jpg")
        sys.exit()
    img_file = sys.argv[1]
    ext = img_file.split('.')[-1]

    if (ext == 'jpg') | (ext == 'JPG') | (ext == 'jpeg') | (ext == 'JPEG') :
        msg = get_exif(img_file)
        print(msg)
    else:
        print('[-] Not JPEG format . . .')

