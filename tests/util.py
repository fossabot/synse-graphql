""" Utils to help out with testing

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import json
import logging
import os

import graphene.test
import testtools

import synse_graphql.config
import synse_graphql.schema
from synse_graphql.log import setup_logging

QUERY_PREVIEW_LENGTH = 1000


class BaseSchemaTest(testtools.TestCase):

    def setUp(self):
        super(BaseSchemaTest, self).setUp()
        setup_logging({
            'version': 1,
            'disable_existing_loggers': False
        })

        synse_graphql.config.parse_args([
            '--backend',
            'backend;;http://synse-server:5000'
        ])
        self.client = graphene.test.Client(synse_graphql.schema.create())

    def get_query(self, name):
        path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), "queries", "{0}.graphql".format(name)))
        with open(path, "r") as fobj:
            return fobj.read()

    def output(self, result):
        print(json.dumps(result.get('data'), indent=4)[:QUERY_PREVIEW_LENGTH])

    def assertQuery(self, result):
        if result.get('errors') is None:
            result['errors'] = []

        for error in result['errors']:
            logging.exception("Query error", exc_info=error)
            if hasattr(error, "message"):
                logging.debug(error.message)

        self.assertFalse(result['errors'])
        self.output(result)

    def run_query(self, name, params=None):
        result = self.client.execute(
            self.get_query(name), variable_values=params)
        self.assertQuery(result)
        return result
