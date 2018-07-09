""" Utils to help out with building schemas

    Author: Thomas Rampelberg
    Date:   2/27/2017
"""

import concurrent.futures
import logging

import requests
import requests.compat

from synse_graphql import config

SESSION = requests.Session()

logger = logging.getLogger(__name__)


def scan():
    """Scan every backend and return the full device list.

    Returns:
        dict: Synse server scan results
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [executor.submit(lambda: (b, make_request(b, 'scan')))
                 for b in config.options.get('backend').keys()]
        for future in concurrent.futures.as_completed(tasks):
            try:
                scan_result = future.result()
                yield scan_result
            except Exception as ex:
                logger.exception(ex)


def make_version_request(backend):
    """ Request api version for provided backend, set entry in config

    Args:
        backend (str): backend to make the request for

    Returns:
        str: synse-server api version
    """
    _backend = config.options.get('backend').get(backend)
    try:
        r = SESSION.get(
            '{}/synse/version'.format(_backend.get('host')),
            timeout=config.options.get('timeout'))
        r.raise_for_status()
        _backend['api_version'] = r.json().get('api_version')
        return _backend.get('api_version')
    except Exception as ex:
        logging.exception('Request failure [{} version] : {}'.format(
            backend, ex))
        raise ex


def make_request(backend, uri):
    """Make a request to the provided URI.

    Args:
        backend (str): backend to make the request for.
        uri (str): the uri to make the request for.

    Returns:
        the JSON loaded result from the request.
    """
    bundle_path = config.options.get('cert_bundle')
    if bundle_path:
        SESSION.cert = bundle_path

    ca_path = config.options.get('ssl_verify')
    if ca_path:
        SESSION.verify = ca_path

    _backend = config.options.get('backend').get(backend)
    if _backend.get('api_version') is None:
        make_version_request(backend)

    api_version = _backend.get('api_version')
    base = '{0}/synse/{1}/'.format(_backend.get('host'), api_version)
    try:
        result = SESSION.get(
            requests.compat.urljoin(base, uri),
            timeout=config.options.get('timeout'))
        if result.status_code == 404:
            logger.warning(
                'Clearing API Version [{} {}]'.format(backend, result.text))
            _backend['api_version'] = None
        result.raise_for_status()
    except Exception as ex:
        logging.exception('Request failure [{} {}] : {}'.format(
            backend, uri, ex))
        raise ex

    return result.json()


def get_asset(self, asset, *args, **kwargs):  # pylint: disable=unused-argument
    """Fetch the value for a specific asset.

    Gets converted into resolve_asset_name(). See _assets for the list that
    are using this method as resolve.
    """
    return self._request_assets().get(asset, '')


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
