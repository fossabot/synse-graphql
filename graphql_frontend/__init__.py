#!/usr/bin/env python
""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""
import logging

from flask import Flask
from vapor_common.vapor_logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging(default_path='logging.json')

app = Flask(__name__)


def main():
    app.run(host='0.0.0.0')
