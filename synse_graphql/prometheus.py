""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    4/7/2017
"""

import logging
from datetime import datetime
from string import punctuation

import graphene.test
import graphql.execution.executors.gevent
import prometheus_client
import prometheus_client.exposition
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_client.core import _INF
from pytz import utc

import synse_graphql.schema

query = '''{
    racks {
        id
        backend
        boards {
            id
            devices {
                id
                info
                device_type
                readings {
                    reading_type
                    value
                }
            }
        }
    }
}'''

_metrics = {
    'histogram': {},
    'gauge': {}
}


class Device(object):
    """ Generates prometheus metrics from GraphQL responses
    """

    default_labels = [
        'backend_name',
        'rack_id',
        'board_id',
        'device_id',
        'device_info',
        'device_type'
    ]

    _buckets = {
        'airflow': [0, _INF],
        'pressure': [0, _INF],
        'fan': list(range(0, 8500, 500)) + [_INF],
        'humidity': [0, _INF],
        'temperature': list(range(0, 95, 5)) + [_INF],
        'frequency': [0, _INF],
        'voltage': [0, _INF],
        'current': [0, _INF],
        'power': [0, _INF],
    }

    def __init__(self, rack, board, device):
        self._rack = rack
        self._board = board
        self._device = device
        if self._device.get('readings'):
            self._readings = [
                (r.get('reading_type'), r.get('value'))
                for r in self._device.get('readings')
            ]
        else:
            self._readings = None

    @property
    def type(self):
        return self._device.get('device_type')

    @property
    def labels(self):
        return [
            self._rack.get('backend'),
            self._rack.get('id'),
            self._board.get('id'),
            self._device.get('id'),
            self._device.get('info'),
            self.type
        ]

    def name(self, _type, param):
        """ Construct prometheus metric label from sanitized device attributes
        """
        return 'device_{}'.format('_'.join([
            ''.join(char for char in label if char not in punctuation)
            for label in [self.type, _type, param]]))

    def histogram(self, name):
        return prometheus_client.Histogram(
            name,
            '',
            self.default_labels,
            buckets=self._buckets.get(self.type))

    def gauge(self, name):
        return prometheus_client.Gauge(name, '', self.default_labels)

    def get_metric(self, _type, param):
        name = self.name(_type, param)
        if name not in _metrics.get(_type):
            _metrics.get(_type)[name] = getattr(self, _type)(name)

        return _metrics.get(_type).get(name).labels(*self.labels)

    def record(self):
        """ Verify reading values are numeric and create metrics
        """
        if not self._readings:
            return
        for r in self._readings:
            try:
                float(r[1])
            except ValueError:
                logging.warning('Omitting non-numeric metric [{} {}]'.format(
                    r[0], r[1]))
                continue

            try:
                _type, _value = r
                self.get_metric('gauge', _type).set(float(_value))
                self.get_metric('histogram', _type).observe(float(_value))
            except Exception as ex:
                logging.exception(
                    'failed to log metric [{0}] : {1}'.format(self.type, ex))


class LedDevice(Device):
    """ Handler for LED device_type
    """

    _handlers = {
        'color': lambda x: int(x, 16),
        'state': lambda x: ['off', 'on', 'blink'].index(x),
    }

    def record(self):
        """ Converts LED device readings into numeric values via _handlers
        """
        if not self._readings:
            return
        for r in self._readings:
            try:
                _type, _value = r
                self.get_metric('gauge', _type).set(
                    self._handlers.get(_type)(_value))
            except Exception as ex:
                logging.exception(
                    'failed to log metric [{0}] : {1}'.format(self.type, ex))


summary = prometheus_client.Summary('device_refresh_seconds', '')

handlers = {
    'led': LedDevice,
}


@summary.time()
def get():
    client = graphene.test.Client(synse_graphql.schema.create())
    result = client.execute(
        query,
        executor=graphql.execution.executors.gevent.GeventExecutor())

    for error in result.get('errors', []):
        logging.exception('Query error in Prometheus export ', exc_info=error)
        if hasattr(error, 'message'):
            logging.debug(error.message)

        logging.error('Prometheus export query failed')
        return

    for rack in result.get('data').get('racks'):
        if not rack:
            continue
        for board in rack.get('boards'):
            if not board:
                continue
            for device in board.get('devices'):
                if not device:
                    continue
                handlers.get(device.get('device_type'), Device)(
                    rack, board, device).record()


def refresh():
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(
        get,
        'interval',
        minutes=1,
        next_run_time=datetime.now(utc))
    scheduler.start()


def metrics():
    return prometheus_client.exposition.generate_latest()
