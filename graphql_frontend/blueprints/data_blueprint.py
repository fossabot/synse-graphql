""" Data endpoint for graphql responses

    Author: Thomas Rampelberg
    Date:   2/24/2017

    \\//
     \/apor IO
"""
import logging

from flask import Blueprint

logger = logging.getLogger(__name__)
blueprint = Blueprint('data_blueprint', __name__)


# This needs to be updated.
@blueprint.route("/graphql")
def get_graph():
    return "asdf"
