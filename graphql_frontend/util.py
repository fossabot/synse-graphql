""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import logging
import sys


def init_logging(level="info"):
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, level.upper()))
