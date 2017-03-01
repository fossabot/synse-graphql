""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
import json
import testtools

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

    def test_cluster(self):
        result = self.run_query("""{
            clusters {
                id
            }
        }
        """)
        clusters = result.data.get("clusters", [])
        self.assertTrue(clusters)
        self.assertItemsEqual(clusters[0].keys(), ["id"])
