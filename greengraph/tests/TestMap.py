from greengraph.classes.Map import Map as Map
import requests
from matplotlib import image as img
import mock
import StringIO
from unittest import TestCase


class TestMap(TestCase):

    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        pass

    @classmethod
    def teardown_class(cls):
        """This method is run once for each class _after_ all tests are run"""
        pass

    def setUp(self):
        """This method is run once before _each_ test method is executed"""
        pass

    def tearDown(self):
        """This method is run once after _each_ test method is executed"""
        pass

    @mock.patch.object(requests, 'get', autospec=True)
    @mock.patch.object(img, 'imread', autospec=True)
    def test_init(self, mock_imread, mock_get):

        default_map = Map(51.0, 1.0)

        # Assert default parameters passed to requests get object
        mock_get.assert_called_with(
        "http://maps.googleapis.com/maps/api/staticmap?",
        params=dict(
            sensor=str(False).lower(),
            zoom=10,
            size="x".join(map(str, (400, 400))),
            center=",".join(map(str, (51.0, 1.0))),
            style="feature:all|element:labels|visibility:off",
            maptype="satellite"
        )
        )

        # Check StringIO object read in by imread
        args, kwargs = mock_imread.call_args
        self.assertTrue(isinstance(args[0], StringIO.StringIO))


    def test_green(self):
        pass

    def test_count_green(self):
        pass

    def test_show_green(self):
        pass
