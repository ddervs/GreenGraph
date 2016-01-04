from greengraph.classes.Greengraph import Greengraph
from unittest import TestCase
import geopy
import mock
import yaml
import os
import numpy as np
from greengraph.classes.Map import Map

class TestGreengraph(TestCase):

    def __init__(self, *args, **kwargs):

        super(TestGreengraph, self).__init__(*args, **kwargs)

        self.start = 'New York'
        self.end = 'London'

        with mock.patch.object(geopy.geocoders, 'GoogleV3', autospec=True) as mock_geocoder:
            self.mock_greengraph = Greengraph(self.start, self.end)

    @mock.patch.object(geopy.geocoders, 'GoogleV3', autospec=True)
    def test_init(self, mock_geocoder):

        Greengraph(self.start, self.end)
        mock_geocoder.assert_called_with(domain="maps.google.co.uk")

    @mock.patch.object(geopy.geocoders.GoogleV3, 'geocode')
    def test_geolocate(self, mock_geocode):

        place = self.start
        Greengraph(self.start, self.end).geolocate(place)
        mock_geocode.assert_called_with(place, exactly_one=False)

    def test_location_sequence(self):

        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'location_sequence_fixtures.yaml'))\
                as fixtures_file:
            fixtures = yaml.load(fixtures_file)
            for fixture in fixtures:
                start = fixture.pop('start')
                end = fixture.pop('end')
                steps = fixture.pop('steps')
                result = np.array(fixture.pop('result'))
                # Check result as given in fixtures file
                self.assertTrue((self.mock_greengraph.location_sequence(start, end, steps) == result).all())

    @mock.patch.object(Greengraph, 'geolocate')
    @mock.patch.object(Map, 'count_green')
    def test_green_between(self, mock_count_green, mock_geolocate):

        with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'green_between_fixtures.yaml')) as fixtures_file:
            fixtures = yaml.load(fixtures_file)
            for fixture in fixtures:
                start = fixture.pop('start')
                end = fixture.pop('end')
                steps = fixture.pop('steps')
                start_location = fixture.pop('start_location')
                end_location = fixture.pop('end_location')
                green_counts = fixture.pop('green_counts')

                # Tell mocks the output of geolocate() and count_green() methods for given input
                mock_geolocate.side_effect = [start_location, end_location]
                mock_count_green.side_effect = green_counts
                # Number of green pixels for each step, i.e. what is plotted
                greens = Greengraph(start, end).green_between(steps)
                # Check that output is same as predicted
                self.assertTrue(greens == green_counts)
