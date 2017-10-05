#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

from flask import Flask, make_response
from flask_graphql import GraphQLView

from synse_graphql import config, schema

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

    app.run(host='0.0.0.0', port=config.options.get('port'))
