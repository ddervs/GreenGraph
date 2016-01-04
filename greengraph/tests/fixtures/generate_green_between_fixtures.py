import numpy as np
import requests
from StringIO import StringIO
from matplotlib import image as img
import geopy


# First put in code needed for green_between code
class Map(object):

    def __init__(self, latitude, longitude, satellite=True,
                 zoom=10, size=(400, 400), sensor=False):

        base = "http://maps.googleapis.com/maps/api/staticmap?"

        params = dict(
                sensor=str(sensor).lower(),
                zoom=zoom,
                size="x".join(map(str, size)),
                center=",".join(map(str, (latitude, longitude))),
                style="feature:all|element:labels|visibility:off"
        )

        if satellite:
            params["maptype"] = "satellite"
        self.image = requests.get(base, params=params).content
        # Fetch our PNG image data
        self.pixels = img.imread(StringIO(self.image))

    # Parse our PNG image as a numpy array
    def green(self, threshold):

        # Use NumPy to build an element-by-element logical array
        greener_than_red = self.pixels[:, :, 1] > threshold * self.pixels[:, :, 0]
        greener_than_blue = self.pixels[:, :, 1] > threshold * self.pixels[:, :, 2]
        green = np.logical_and(greener_than_red, greener_than_blue)
        return green

    def count_green(self, threshold=1.1):

        return np.sum(self.green(threshold))


class Greengraph(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.geocoder = geopy.geocoders.GoogleV3(
                domain="maps.google.co.uk")

    def geolocate(self, place):
        return self.geocoder.geocode(place,
                                     exactly_one=False)[0][1]

    def location_sequence(self, start, end, steps):
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1], end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        return [Map.Map(*location).count_green()
                for location in self.location_sequence(
                    self.geolocate(self.start),
                    self.geolocate(self.end),
                    steps)]

my_graph = Greengraph('New York', 'London')
steps = 10
for location in