""" Tests for the device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestDevice(BaseSchemaTest):

    def test_query(self):
        result = self.run_query("test_devices")
        assert False
