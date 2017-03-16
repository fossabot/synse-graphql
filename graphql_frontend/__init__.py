#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""
import importlib
import logging

from flask import Flask

from vapor_common.vapor_logging import setup_logging

from . import blueprints

logger = logging.getLogger(__name__)
setup_logging(default_path='logging.json')

app = Flask(__name__)

# thomasr: I'm not proud of this ... definitely needs refactoring.
for name in blueprints.__all__:
    if name == "__init__":
        continue
    app.register_blueprint(
        getattr(importlib.import_module(
            "graphql_frontend.blueprints.{0}".format(name)), "blueprint"))


def main():
    app.run(host='0.0.0.0')
