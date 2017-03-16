#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""
from gevent import monkey; monkey.patch_socket() # noqa

from graphql_frontend import config
from graphql_frontend import main


if __name__ == '__main__':
    config.parse_args()
    main()
