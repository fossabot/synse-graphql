#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

from flask import Flask, make_response
from flask_graphql import GraphQLView

from synse_graphql import config
from synse_graphql import prometheus
from synse_graphql import schema


app = Flask(__name__)


@app.route('/test')
def test():
    return make_response('ok')


def main():
    local_schema = schema.create()

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=local_schema,
            graphiql=True))

    app.add_url_rule(
        '/metrics',
        view_func=prometheus.metrics
        )

    prometheus.refresh()

    app.run(host='0.0.0.0', port=config.options.get('port'))
