""" Utils to help out with testing

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import json
import logging
import os
import testtools

import graphql_frontend.schema


class BaseSchemaTest(testtools.TestCase):

    def setUp(self):
        super(BaseSchemaTest, self).setUp()
        self.schema = graphql_frontend.schema.create()

    def get_query(self, name):
        path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "queries", "{0}.graphql".format(name)))
        with open(path, "r") as fobj:
            return fobj.read()

    def output(self, result):
        print(json.dumps(result.data, indent=4)[:2000])

    def assertQuery(self, result):
        for error in result.errors:
            logging.exception("Query error", exc_info=error)
            if hasattr(error, "message"):
                logging.debug(error.message)
        self.assertFalse(result.errors)
        self.output(result)

    def run_query(self, name):
        result = self.schema.execute(self.get_query(name))
        self.assertQuery(result)
        return result
