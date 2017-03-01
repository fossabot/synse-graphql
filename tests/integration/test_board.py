""" Tests for the board schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestBoard(BaseSchemaTest):

    def test_query(self):
        keys = ["id"]
        result = self.run_query("test_boards")
        board = result.data["clusters"][0]["racks"][0]["boards"][0]
        self.assertItemsEqual(board.keys(), keys)
