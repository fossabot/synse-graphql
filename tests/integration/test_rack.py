""" Tests for the rack schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestRack(BaseSchemaTest):

    def test_query(self):
        keys = [
            "id",
            "is_leader",
            "is_shadow",
            "vec_ip",
            "failed_servers",
            "server_count"
        ]
        result = self.run_query("test_racks")
        rack = result.data["clusters"][0]["racks"][0]
        self.assertItemsEqual(rack.keys(), keys)
