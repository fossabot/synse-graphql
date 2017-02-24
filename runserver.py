#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""
from gevent import monkey; monkey.patch_socket() # noqa

from graphql_frontend import main

main()
