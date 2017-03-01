""" Tests for the notification schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestNotification(BaseSchemaTest):

    def test_query(self):
        keys = [
            "_id",
            "code",
            "resolved_on",
            "severity",
            "source",
            "status",
            "text",
            "timestamp"
        ]
        source_keys = [
            "BoardID",
            "DeviceID",
            "DeviceType",
            "Field",
            "RackID",
            "Reading",
            "ZoneID"
        ]
        result = self.run_query("test_notifications")
        notification = result.data.get("notifications", [])[0]
        self.assertItemsEqual(notification.keys(), keys)
        self.assertItemsEqual(notification.get("source", {}), source_keys)
