import numpy as np
import requests
from StringIO import StringIO
from matplotlib import image as img
import geopy
import yaml


# First hard-code what is needed for correct output of green_between()
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


# Now build fixtures method
def build_fixture(start, end, steps):

    my_graph = Greengraph(start, end)
    locations = my_graph.location_sequence(
                    my_graph.geolocate(my_graph.start),
                    my_graph.geolocate(my_graph.end),
                    steps)

    green_counts = [None]*len(locations)
    for i in range(0, len(locations)):
        location = locations[i]
        green_counts[i] = Map(*location).count_green()

    start_location = my_graph.geolocate(my_graph.start)
    end_location = my_graph.geolocate(my_graph.end)

    return eval(str(dict(start=start, end=end, start_location=start_location, end_location=end_location,
                         green_counts=green_counts, steps=steps)))


# Write YAML file
with open('green_between_fixtures.yaml', 'w') as file_to_write:
    file_to_write.write(yaml.dump([build_fixture('Paris', 'Chicago', 10)]))
    file_to_write.write(yaml.dump([build_fixture('Matlab', 'Bangkok', 10)]))
    file_to_write.write(yaml.dump([build_fixture('London', 'Bristol', 10)]))


