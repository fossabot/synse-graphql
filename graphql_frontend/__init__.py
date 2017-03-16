#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""
import logging

from flask import Flask
from flask_graphql import GraphQLView

import graphql_frontend.config
import graphql_frontend.schema
from vapor_common.vapor_logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging(default_path='logging.json')

app = Flask(__name__)
local_schema = graphql_frontend.schema.create()

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=local_schema,
        graphiql=True))


def main():
    app.run(host='0.0.0.0', port=graphql_frontend.config.options.get('port'))
