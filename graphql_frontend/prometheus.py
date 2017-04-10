""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    4/7/2017

    \\//
     \/apor IO
"""

import logging

import prometheus_client
import prometheus_client.exposition

import graphql_frontend.schema


query = '''{
    clusters {
        id
        racks {
            id
            is_leader
            is_shadow
            vec_ip
            failed_servers
            server_count
            boards {
                id
                devices {
                    id
                    info
                    device_type
                    ... on TemperatureDevice {
                        temperature_c
                    }
                    ... on PressureDevice {
                        pressure_kpa
                    }
                    ... on FanSpeedDevice {
                        speed_rpm
                    }
                    ... on PowerDevice {
                        input_power
                    }
                }
            }
        }
    }
}'''

_gauges = {}


class Device(object):

    default_labels = [
        "cluster_id",
        "rack_id",
        "board_id",
        "device_id",
        "device_info",
        "device_type"
    ]

    _filter_keys = [
        "id",
        "info",
        "device_type"
    ]

    def __init__(self, cluster, rack, board, device):
        self._cluster = cluster
        self._rack = rack
        self._board = board
        self._device = device

    def gauge(self, param):
        name = 'device_{0}_{1}'.format(self._device.get('device_type'), param)
        if name not in _gauges:
            _gauges[name] = prometheus_client.Gauge(
                name,
                '',
                self.default_labels)

        return _gauges.get(name).labels(
            self._cluster.get("id"),
            self._rack.get("id"),
            self._board.get("id"),
            self._device.get("id"),
            self._device.get("info"),
            self._device.get("device_type"))

    def record(self):
        for k, v in self._device.items():
            if k in self._filter_keys:
                continue
            self.gauge(k).set(v)


def get():
    schema = graphql_frontend.schema.create()
    result = schema.execute(query)

    for error in result.errors:
        logging.exception("Query error", exc_info=error)
        if hasattr(error, "message"):
            logging.debug(error.message)

    for cluster in result.data.get("clusters"):
        if not cluster:
            continue
        for rack in cluster.get("racks"):
            if not rack:
                continue
            for board in rack.get("boards"):
                if not board:
                    continue
                for device in board.get("devices"):
                    if not device:
                        continue
                    Device(cluster, rack, board, device).record()

    return prometheus_client.exposition.generate_latest()
