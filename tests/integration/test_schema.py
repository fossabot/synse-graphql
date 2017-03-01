""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
import json
import testtools

from nose.plugins.attrib import attr

import graphql_frontend.schema


class TestSchema(testtools.TestCase):

    def setUp(self):
        super(TestSchema, self).setUp()
        self.schema = graphene.Schema(
            query=graphql_frontend.schema.System,
            auto_camelcase=False)

    def output(self, result):
        print(json.dumps(result.data, indent=4))

    def assertQuery(self, result):
        for error in result.errors:
            print(error.message)
        self.assertFalse(result.errors)
        self.output(result)

    def run_query(self, query):
        result = self.schema.execute(query)
        self.assertQuery(result)
        return result

    def test_cluster_basic(self):
        result = self.run_query("""{
            clusters {
                id
            }
        }
        """)
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
        result = self.run_query("""{
            clusters {
                id
                hardware_version
                leader_service_profile
                model_number
                serial_number
                vendor
            }
        }""")
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
        result = self.run_query("""{
            notifications {
                _id
                code
                resolved_on
                severity
                source {
                    BoardID
                    DeviceID
                    DeviceType
                    Field
                    RackID
                    Reading
                    ZoneID
                }
                status
                text
                timestamp
            }
        }""")
        notification = result.data.get("notifications", [])[0]
        self.assertItemsEqual(notification.keys(), keys)
        self.assertItemsEqual(notification.get("source", {}), source_keys)

    @attr("now")
    def test_racks(self):
        keys = [
            "id",
            "is_leader",
            "is_shadow",
            "vec_ip",
            "failed_servers",
            "server_count"
        ]
        result = self.run_query("""{
            clusters {
                racks {
                    id
                    is_leader
                    is_shadow
                    vec_ip
                    failed_servers
                    server_count
                }
            }
        }""")
        rack = result.data["clusters"][0]["racks"][0]
        self.assertItemsEqual(rack.keys(), keys)
