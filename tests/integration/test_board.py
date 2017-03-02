""" Tests for the board schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestBoard(BaseSchemaTest):

    def get_boards(self, query):
        return self.run_query(query).data["clusters"][0]["racks"][0]["boards"]

    def test_query(self):
        keys = ["id"]
        self.assertItemsEqual(self.get_boards("test_boards")[0].keys(), keys)