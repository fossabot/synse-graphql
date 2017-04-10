""" GraphQL Frontend

    Author:  Thomas Rampelberg
    Date:    4/7/2017

    \\//
     \/apor IO
"""

import prometheus_client
import prometheus_client.exposition

import graphql_frontend.schema

# query = '''{
#     clusters {
#         id
#         hardware_version
#         leader_service_profile
#         model_number
#         serial_number
#         vendor
#         racks {
#             id
#             is_leader
#             is_shadow
#             vec_ip
#             failed_servers
#             server_count
#             boards {
#                 id
#                 devices {
#                     id
#                     device_type
#                     location {
#                         chassis_location {
#                             depth
#                             vert_pos
#                             horiz_pos
#                             server_node
#                         }
#                         physical_location {
#                             depth
#                             horizontal
#                             vertical
#                         }
#                     }
#                     ... on FanSpeedDevice {
#                         fan_mode
#                         speed_rpm
#                     }
#                     ... on LedDevice {
#                         led_state
#                     }
#                     ... on PowerDevice {
#                         input_power
#                         input_voltage
#                         output_current
#                         over_current
#                         pmbus_raw
#                         power_ok
#                         power_status
#                         under_voltage
#                     }
#                     ... on PressureDevice {
#                         pressure_kpa
#                     }
#                     ... on TemperatureDevice {
#                         temperature_c
#                     }
#                     ... on VaporFanDevice {
#                         fan_mode
#                         speed_rpm
#                     }
#                     ... on VaporLedDevice {
#                         blink_state
#                         led_color
#                         led_state
#                     }
#                     ... on VaporRectifierDevice {
#                         input_power
#                         input_voltage
#                         output_current
#                         over_current
#                         pmbus_raw
#                         power_ok
#                         power_status
#                         under_voltage
#                     }
#                 }
#             }
#         }
#     }
# }'''

                    # ... on PowerDevice {
                    #     input_power
                    #     input_voltage
                    #     output_current
                    #     over_current
                    #     power_ok
                    #     under_voltage
                    # }
                    # ... on FanSpeedDevice {
                    #     speed_rpm
                    # }
                    # ... on PressureDevice {
                    #     pressure_kpa
                    # }

query = '''{
    clusters {
        id
        hardware_version
        leader_service_profile
        model_number
        serial_number
        vendor
        racks(id:"rack_1") {
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
                    device_type
                    ... on TemperatureDevice {
                        temperature_c
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
    ]

    _filter_keys = [
        "id",
        "device_type"
    ]

    def __init__(self, cluster, rack, board, device):
        self._cluster = cluster
        self._rack = rack
        self._board = board
        self._device = device

    def gauge(self, param):
        name = 'device_{}_{}'.format(self._device.get('device_type'), param)
        if name not in _gauges:
            _gauges[name] = prometheus_client.Gauge(
                name,
                '',
                self.default_labels)

        return _gauges.get(name).labels(
            self._cluster.get("id"),
            self._rack.get("id"),
            self._board.get("id"),
            self._device.get("id"))

    def record(self):
        for k, v in self._device.items():
            if k in self._filter_keys:
                continue
            self.gauge(k).set(v)


def get():
    schema = graphql_frontend.schema.create()
    result = schema.execute(query)

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
