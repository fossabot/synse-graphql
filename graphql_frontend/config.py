""" Configuration

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

import configargparse


parser = configargparse.ArgParser(default_config_files=[
    "/graphql_frontend/config.yaml"
])
parser.add('-c', '--my-config', is_config_file=True, help='config file path')
parser.add(
    '--port',
    env_var='PORT',
    required=True,
    help='Port to listen on.')
parser.add(
    '--router_server',
    env_var='ROUTER_SERVER',
    required=True,
    help='Path to the router to use. example: "172.17.0.1:4998"')
parser.add(
    '--username',
    env_var='AUTH_USERNAME',
    required=True,
    help='Username to use when authenticating against the router.')
parser.add(
    '--password',
    env_var='AUTH_PASSWORD',
    required=True,
    help='Password to use when authenticating against the router.')

options = None


def parse_args(opts=None):
    global options
    options = vars(parser.parse_args(opts))
