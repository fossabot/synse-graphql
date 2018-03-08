""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    4/7/2017

    \\//
     \/apor IO
"""

import logging
from datetime import datetime

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
                ... on AirflowDevice {
                  airflow
                }
                ... on DifferentialPressureDevice {
                  pressure
                }
                ... on FanDevice {
                    fan_speed
                }
                ... on HumidityDevice {
                  humidity
                }
                ... on LedDevice {
                    blink
                    color
                    state
                }
                ... on TemperatureDevice {
                    temperature
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

    default_labels = [
        'backend_name',
        'rack_id',
        'board_id',
        'device_id',
        'device_info',
        'device_type'
    ]

    _filter_keys = [
        'id',
        'info',
        'device_type'
    ]

    _buckets = {
        'airflow': [0, _INF],
        'differential_pressure': [0, _INF],
        'fan': list(range(0, 8500, 500)) + [_INF],
        'humidity': [0, _INF],
        'temperature': list(range(0, 95, 5)) + [_INF],
    }

    def __init__(self, rack, board, device):
        self._rack = rack
        self._board = board
        self._device = device

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
        return 'device_{0}_{1}_{2}'.format(self.type, _type, param)

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
        for k, v in self._device.items():
            if k in self._filter_keys:
                continue
            try:
                self.get_metric('gauge', k).set(v)
                self.get_metric('histogram', k).observe(v)
            except Exception as ex:
                logging.exception(
                    'failed to log metric: {0}'.format(self.type))


class LedDevice(Device):

    _handlers = {
        'blink': lambda x: 0 if x == 'steady' else 1,
        'color': lambda x: int(x, 16),
        'state': lambda x: 0 if x == 'off' else 1,
    }

    def record(self):
        for k, v in self._device.items():
            if k in self._filter_keys:
                continue
            try:
                self.get_metric('gauge', k).set(self._handlers.get(k)(v))
            except Exception as ex:
                logging.exception(
                    'failed to log metric: {0}'.format(self.type))


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
        logging.exception('Query error', exc_info=error)
        if hasattr(error, 'message'):
            logging.debug(error.message)

        logging.error('Query failed')
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
