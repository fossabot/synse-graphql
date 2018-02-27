""" Tests for the device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr  # noqa

from ..util import BaseSchemaTest


class TestDevice(BaseSchemaTest):

    def get_devices(self, query):
        return self.run_query(query).get('data').get(
            "racks")[0].get("boards")[0].get("devices")

    def check_keys(self, data, keys):
        self.assertItemsEqual(data.keys(), keys.keys())
        for k, v in keys.items():
            if len(v.keys()) > 0:
                self.check_keys(data.get(k), keys.get(k))

    def test_basic_query(self):
        keys = {
            "id": {},
            "device_type": {},
        }

        self.check_keys(self.get_devices("test_devices")[0], keys)

    def test_type_arg(self):
        self.assertEqual(len(self.get_devices("test_device_type_arg")), 5)

    def test_airflow(self):
        keys = [
            "airflow"
        ]
        self.assertItemsEqual(
            self.get_devices("test_airflow_device")[0].keys(), keys)

    def test_differential_pressure(self):
        keys = [
            "pressure"
        ]
        self.assertItemsEqual(
            self.get_devices(
                "test_differential_pressure_device")[0].keys(), keys)

    def test_humidity(self):
        keys = [
            "humidity"
        ]
        self.assertItemsEqual(
            self.get_devices("test_humidity_device")[0].keys(), keys)

    def test_temperature(self):
        keys = ["temperature"]
        self.assertItemsEqual(
            self.get_devices("test_temp_device")[0].keys(), keys)

    def test_led(self):
        keys = [
            "blink",
            "color",
            "state"
        ]
        self.assertItemsEqual(
            self.get_devices("test_led_device")[0].keys(), keys)

    def test_fan(self):
        keys = [
            "fan_speed"
        ]
        self.assertItemsEqual(
            self.get_devices("test_fan_device")[0].keys(), keys)
