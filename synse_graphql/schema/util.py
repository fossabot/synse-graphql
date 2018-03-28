""" Utils to help out with building schemas

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import concurrent.futures
import functools
import logging

import requests
import requests.compat
from requests.exceptions import HTTPError

from synse_graphql import config

SESSION = requests.Session()

logger = logging.getLogger(__name__)


def scan():
    """Scan every backend and return the full device list.

    Returns:
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [executor.submit(lambda: (b, make_request(b, 'scan')))
                 for b in config.options.get('backend').keys()]
        for future in concurrent.futures.as_completed(tasks):
            yield future.result()


def make_request(backend, uri):
    """Make a request to the provided URI.

    Args:
        uri (str): the uri to make the request for.

    Returns:
        the JSON loaded result from the request.
    """
    version = config.options.get('version')
    path = config.options.get('backend').get(backend)
    bundle_path = config.options.get('cert_bundle')
    if bundle_path:
        SESSION.cert = bundle_path

    ca_path = config.options.get('ssl_verify')
    if ca_path:
        SESSION.verify = ca_path

    # if the version is unspecified, we'll have to get the version
    # from the synse instance.
    if version is None:
        r = SESSION.get(
            '{}/synse/version'.format(path),
            timeout=config.options.get('timeout'))
        if r.ok:
            version = r.json().get('api_version')
        else:
            logger.warning('Unable to get API version of Synse.')
            r.raise_for_status()

    base = '{0}/synse/{1}/'.format(path, version)
    try:
        result = SESSION.get(
            requests.compat.urljoin(base, uri),
            timeout=config.options.get('timeout'))
        result.raise_for_status()
    except Exception as ex:
        logging.exception('Request failure')
        raise ex

    return result.json()


def get_asset(self, asset, *args, **kwargs):  # pylint: disable=unused-argument
    """Fetch the value for a specific asset.

    Gets converted into resolve_asset_name(). See _assets for the list that
    are using this method as resolve.
    """
    return self._request_assets().get(asset, '')


# FIXME -- unused?
def resolve_assets(cls):
    """Decorator to dynamically resolve fields.

    Add resolve methods for everything in _assets.
    """
    for asset in cls._assets:
        setattr(
            cls,
            'resolve_{0}'.format(asset),
            functools.partialmethod(get_asset, asset))
    return cls


def arg_filter(val, fn, lst):
    """

    Args:
        val ():
        fn ():
        lst ():

    Returns:
        list:
    """
    if val is not None:
        return filter(fn, lst)
    return lst
