""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestSchema(BaseSchemaTest):

    def test_cluster_basic(self):
        result = self.run_query("test_cluster_basic")
        clusters = result.data.get("clusters", [])
        self.assertTrue(clusters)
        self.assertItemsEqual(clusters[0].keys(), ["id"])

    def test_cluster_all(self):
        keys = [
            "id",
            "hardware_version",
            "leader_service_profile",
            "model_number",
            "serial_number",
            "vendor"
        ]
        result = self.run_query("test_cluster_all")
        cluster = result.data.get("clusters", [])[0]
        self.assertItemsEqual(cluster.keys(), keys)

    def test_notifications(self):
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

    def test_racks(self):
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
