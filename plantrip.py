#! python3
"""Eases planning of short vacations by gathering information on the destination of the trip and its surroundings."""
import sys
import webbrowser, datetime, time
from selenium import webdriver

# Find date of next friday for controlling parts of Shortttrip.getinfo() and for setting the default starting date of Shorttrip objects:
today = datetime.date.today()
weekday = datetime.datetime.isoweekday(today)
days2friday = datetime.timedelta(days = 5 - weekday)
nextfriday = today + days2friday

#Define Shorttrip class and class methods:
class Shorttrip(object):
    def __init__(self, place="tuebingen", startdate=nextfriday, nodays=2):
        self.__Place = place
        self.__Startdate = startdate
        self.__Nodays = nodays
    def getinfo(self):
        # Wikipedia-Eintrag aufmachen:
        webbrowser.open("https://de.wikipedia.org/wiki/" + self.__Place)
        time.sleep(1)
        # Mache Klimatabelle auf:
        webbrowser.open("https://www.google.de/search?q=" + self.__Place + "+klimatabelle&tbm=isch")
        time.sleep(1)
        # Berechne Anfahrtsdauer mit dem Auto:
        webbrowser.open("https://www.google.de/maps/dir/tuebingen/" + self.__Place)        
        time.sleep(1)
        # Suche Freizeitangebote heraus:
        webbrowser.open("https://www.google.de/search?q=" + self.__Place + "+freizeit")
        time.sleep(1)
        # Checke das Wetter:
        webbrowser.open("https://www.google.de/search?q=" + self.__Place + "+wetter")
    def param(self):
        return (self.__Place, self.__Startdate.strftime("%Y-%m-%d"), self.__Nodays)
    def getGPS(self):
        #1. go to: http://www.whatsmygps.com/
        browser = webdriver.Firefox()
        browser.get("http://www.whatsmygps.com/")
        #2 fill in self.__Place into box above "Find This Location"
        placeElem = browser.find_element_by_id("address")
        placeElem.send_keys(self.__Place)
        #2b: Click on that field.
        placeElem.submit()
        #3 Grab Latitude and Longitude in the boxes right to the respective text descriptors.
        latElem = browser.find_element_by_id("latitude")
        latitude = latElem.get_attribute("value")
        lonElem = browser.find_element_by_id("longitude")
        longitude = lonElem.get_attribute("value")
        browser.close()
        return (latitude, longitude)
    def getphotos(self, latitude=48.521636, longitude=9.057645):
        """Gathers the best photos for a given place within a given distance by searching google, flickr and 500px. 
        Results are displayed on a map in a web browser."""
        webbrowser.open("https://www.google.de/search?q=" + self.__Place + "&tbm=isch")
        time.sleep(1)
        webbrowser.open("https://www.flickr.com/search/?q=" + self.__Place + "&tbm=isch")
        time.sleep(1)
        webbrowser.open("https://500px.com/search?q=" + self.__Place + "&type=photos")
        time.sleep(1)
        webbrowser.open("https://www.flickr.com/map/?fLat=" + latitude + "&fLon=" + longitude + "&zl=13&everyone_nearby=1")
        # please note: sorting photos according to search rank, interestingness and pulse is not possible without 
        # losing the sort order according to relevance to the search term, a problem of the photo-providing websites.
        # to be done: Umkreissuche, Suche anhand  GEOkoordinaten, Filtere nur Fotos mit Geotags heraus.
        # TBD: Display photos on a map.


#ToDO: def tourinfo
#3. beste Wandertouren sammeln von komoot, gpsies etc.
#
#ToDo: def findacc
#4. Hotel/Unterkunft passend zum Datum suchen

# Plan specific shorttrip:
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        place = sys.argv[1]
        x = Shorttrip(place = place)     
    else:
        x = Shorttrip()
    print(x.param())
    x.getinfo()
    latlon = x.getGPS()
    latitude = latlon[0]
    longitude = latlon[1]
    x.getphotos(latitude=latitude, longitude=longitude)
    print("done")