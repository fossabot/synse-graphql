""" Utils to help out with building schemas

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import logging

import requests
import requests.compat

from synse_graphql import config

SESSION = requests.Session()

logger = logging.getLogger(__name__)


def make_request(uri):
    """Make a request to the provided URI.

    Args:
        uri (str): the uri to make the request for.

    Returns:
        the JSON loaded result from the request.
    """
    version = config.options.get('version')
    backend = config.options.get('backend')

    # if the version is unspecified, we'll have to get the version
    # from the synse instance.
    if version is None:
        r = requests.get('http://{}/synse/version'.format(backend))
        if r.ok:
            version = r.json().get('version')
        else:
            logger.warning('Unable to get API version of Synse.')
            r.raise_for_status()

    base = 'http://{0}/synse/{1}/'.format(backend, version)
    result = SESSION.get(requests.compat.urljoin(base, uri))
    result.raise_for_status()
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
