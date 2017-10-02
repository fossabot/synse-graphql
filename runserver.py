#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

from synse_graphql import app, config, log


if __name__ == '__main__':
    config.parse_args()
    log.setup_logging()
    app.main()
