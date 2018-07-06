""" Configuration

    Author:  Thomas Rampelberg
    Date:    2/24/2017

    \\//
     \/apor IO
"""

import configargparse

parser = configargparse.ArgParser(
    config_file_parser_class=configargparse.YAMLConfigFileParser,
    default_config_files=['/code/config.yaml'])

backend_help = 'Name/path combination for the backend to use. ' + \
    'example: "backend;;http://demo.vapor.io:5000"'

parser.add('-c', '--my-config', is_config_file=True, help='config file path')
parser.add(
    '--port',
    env_var='PORT',
    default=5050,
    help='Port to listen on.')
parser.add(
    '--backend',
    env_var='BACKEND',
    nargs='+',
    default=['backend;;http://synse-server:5000'],
    help=backend_help)
parser.add(
    '--cert-bundle',
    env_var='CERT_BUNDLE',
    help='Client bundle to use for mutual auth. ' +
         '(should contain both the private key and certificate')
parser.add(
    '--ssl-verify',
    env_var='SSL_VERIFY',
    help='CA certificate to use for verification.')
parser.add(
    '--timeout',
    env_var='TIMEOUT',
    type=int,
    default=1,
    help='Timeout for backend requests.'
)

options = None


def parse_args(opts=None):
    global options
    options = vars(parser.parse_args(opts))

    options['backend'] = {
        b[0]: {'host': b[1]} for b in
        [v.split(';;') for v in options.get('backend')]
    }
