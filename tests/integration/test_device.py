""" Tests for the device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestDevice(BaseSchemaTest):

    def get_device(self, result):
        return result.data["clusters"][0]["racks"][0][
            "boards"][0]["devices"][0]

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
        device = self.get_device(self.run_query("test_devices"))
        self.assertItemsEqual(device.keys(), keys)
        self.assertItemsEqual(
            device.get("location").get("chassis_location").keys(),
            chassis_keys)
        self.assertItemsEqual(
            device.get("location").get("physical_location").keys(),
            physical_keys)

    def test_system_device(self):
        keys = [
            "device_type",
            "ip_addresses",
            "hostnames",
            "asset"
        ]
        device = self.get_device(self.run_query("test_systemdevice"))
        self.assertItemsEqual(device.keys(), keys)

    # def test_other(self):
    #     result = self.run_query("test_device_types")
    #     types = set()
    #     for c in result.data["clusters"]:
    #         for r in c["racks"]:
    #             for b in r["boards"]:
    #                 for d in b["devices"]:
    #                     types.add(d["device_type"])
    #     print(types)
    #     assert False
