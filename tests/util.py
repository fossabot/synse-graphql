""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
import json
import os
import testtools
import traceback

import graphql_frontend.schema


class BaseSchemaTest(testtools.TestCase):

    def setUp(self):
        super(BaseSchemaTest, self).setUp()
        self.schema = graphene.Schema(
            query=graphql_frontend.schema.System,
            auto_camelcase=False)

    def get_query(self, name):
        path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "queries", "{0}.graphql".format(name)))
        with open(path, "r") as fobj:
            return fobj.read()

    def output(self, result):
        print(json.dumps(result.data, indent=4)[:500])

    def assertQuery(self, result):
        for error in result.errors:
            print(str(error))
            print(error.message)
        self.assertFalse(result.errors)
        self.output(result)

    def run_query(self, name):
        result = self.schema.execute(self.get_query(name))
        self.assertQuery(result)
        return result
