""" Configuration

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

import configargparse

parser = configargparse.ArgParser(default_config_files=[
    '/synse_graphql/config.yaml'
])
parser.add('-c', '--my-config', is_config_file=True, help='config file path')
parser.add(
    '--port',
    env_var='PORT',
    default=5001,
    help='Port to listen on.')
parser.add(
    '--backend',
    env_var='BACKEND',
    default='synse-server:5000',
    help='Path to the backend to use. example: "demo.vapor.io:5000"')
parser.add(
    '--version',
    env_var='BACKEND_VERSION',
    default='1.4',
    help='The API version of the Synse instance being connected to.'
)

options = None


def parse_args(opts=None):
    global options
    options = vars(parser.parse_args(opts))