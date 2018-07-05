""" Tests for the device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr  # noqa

from ..util import BaseSchemaTest


class TestDevice(BaseSchemaTest):

    def get_devices(self, query, params=None):
        return self.run_query(query, params).get('data').get(
            'racks')[0].get('boards')[0].get('devices')

    def get_readings(self, query, params=None):
        return [reading for device in self.get_devices(query, params) for
                reading in device.get('readings')]

    def _params(self, device_type):
        return {'deviceType': device_type}

    def check_keys(self, data, keys):
        self.assertItemsEqual(data.keys(), keys.keys())
        for k, v in keys.items():
            if len(v.keys()) > 0:
                self.check_keys(data.get(k), keys.get(k))

    def test_basic_query(self):
        keys = {
            'id': {},
            'device_type': {},
            'readings': {},
        }

        self.check_keys(self.get_devices('test_devices')[0], keys)

    def test_type_arg(self):
        self.assertEqual(len(self.get_devices('test_device_type_arg')), 5)

    def test_airflow(self):
        reading_type = 'airflow'
        self.assertItemsEqual(
            self.get_readings(
                'test_device_type', params=self._params('airflow'))[0].get(
                'reading_type'), reading_type)

    def test_pressure(self):
        reading_type = 'pressure'
        self.assertItemsEqual(
            self.get_readings(
                'test_device_type', params=self._params('pressure'))[0].get(
                'reading_type'), reading_type)

    def test_humidity(self):
        reading_type = 'humidity'
        self.assertItemsEqual(
            self.get_readings(
                'test_device_type', params=self._params('humidity'))[0].get(
                'reading_type'), reading_type)

    def test_temperature(self):
        reading_type = 'temperature'
        self.assertItemsEqual(
            self.get_readings(
                'test_device_type', params=self._params(
                    'temperature'))[0].get('reading_type'), reading_type)

    def test_led(self):
        reading_type = {'color', 'state'}
        self.assertItemsEqual(
            {r.get('reading_type') for r in self.get_readings(
                'test_device_type', params=self._params('led'))},
            reading_type)

    def test_fan(self):
        reading_type = 'speed'
        self.assertItemsEqual(
            self.get_readings(
                'test_device_type', params=self._params('fan'))[0].get(
                'reading_type'), reading_type)
