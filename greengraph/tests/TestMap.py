from greengraph.classes.Map import Map as Map
import requests
from matplotlib import image as img
import mock
import StringIO
from unittest import TestCase
import numpy as np


class TestMap(TestCase):

    def __init__(self, *args, **kwargs):

        super(TestMap, self).__init__(*args, **kwargs)

        with mock.patch.object(requests, 'get') as mock_get:
            with mock.patch.object(img, 'imread') as mock_imread:
                self.mock_map = Map(51.0, 1.0)
                self.threshold = 1.1
                self.pixel_array = np.zeros((3, 3, 3))
                self.mock_map.__setattr__('pixels', self.pixel_array)

    @mock.patch.object(requests, 'get', autospec=True)
    @mock.patch.object(img, 'imread', autospec=True)
    def test_init(self, mock_imread, mock_get):

        Map(51.0, 1.0)
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
        call_args, call_kwargs = mock_imread.call_args
        self.assertTrue(isinstance(call_args[0], StringIO.StringIO))

    def test_green(self):

        # Test green function with all green pixels
        self.pixel_array[:, :, 1] = 1
        self.mock_map.__setattr__('pixels', self.pixel_array)
        self.assertTrue(self.mock_map.green(self.threshold).all())

        # Test green function with all red pixels
        self.pixel_array[:, :, 1] = 0
        self.pixel_array[:, :, 0] = 1
        self.mock_map.__setattr__('pixels', self.pixel_array)
        self.assertFalse(self.mock_map.green(self.threshold).all())

        # Test green function with all blue pixels
        self.pixel_array[:, :, 0] = 0
        self.pixel_array[:, :, 2] = 1
        self.mock_map.__setattr__('pixels', self.pixel_array)
        self.assertFalse(self.mock_map.green(self.threshold).all())

    @mock.patch.object(np, 'sum', autospec=True)
    def test_count_green(self, mock_sum):

        self.mock_map.__setattr__('pixels', self.pixel_array)

        # Check sum of numpy array
        self.mock_map.count_green(self.threshold)
        call_args, call_kwargs = mock_sum.call_args
        self.assertTrue(isinstance(call_args[0], np.ndarray))

    @mock.patch.object(img, 'imsave', autospec=True)
    def test_show_green(self, mock_imsave):

        self.mock_map.show_green(self.threshold)
        call_args, call_kwargs = mock_imsave.call_args

        # Check that saved image arg is RGB array
        array_shape = call_args[1].shape
        self.assertTrue(len(array_shape) == 3)
        self.assertTrue(array_shape[2] == 3)
