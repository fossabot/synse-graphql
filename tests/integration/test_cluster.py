""" Tests for the cluster schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr

from ..util import BaseSchemaTest


class TestCluster(BaseSchemaTest):

    def test_basic_query(self):
        result = self.run_query("test_cluster_basic")
        clusters = result.data.get("clusters", [])
        self.assertTrue(clusters)
        self.assertItemsEqual(clusters[0].keys(), ["id"])

    def test_all_fields(self):
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
