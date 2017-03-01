""" Tests for the device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestDevice(BaseSchemaTest):

    @attr("now")
    def test_basic_query(self):
        keys = [
            "id",
            "device_type",
            "location"
        ]
        chassis_keys = [
            "depth",
            "vert_pos",
            "horiz_pos",
            "server_node"
        ]
        physical_keys = [
            "depth",
            "horizontal",
            "vertical"
        ]
        result = self.run_query("test_devices")
        device = result.data["clusters"][0]["racks"][0][
            "boards"][0]["devices"][0]
        self.assertItemsEqual(device.keys(), keys)
        self.assertItemsEqual(
            device.get("location").get("chassis_location").keys(),
            chassis_keys)
        self.assertItemsEqual(
            device.get("location").get("physical_location").keys(),
            physical_keys)
        assert False
