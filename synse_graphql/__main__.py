#!/usr/bin/env python
"""Entry point for Synse GraphQL.

This entry point script will run when the synse_graphql
module is called directly, e.g.

   $ python synse_graphql

"""

from synse_graphql import app, config, log

config.parse_args()
log.setup_logging()
app.main()
