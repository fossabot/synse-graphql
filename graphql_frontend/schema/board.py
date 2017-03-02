""" Board Schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene

from .device import DeviceInterface, SystemDevice, SensorDevice, PressureDevice


class Board(graphene.ObjectType):
    _data = None
    _type_map = {
        "system": SystemDevice,
        "pressure": PressureDevice
    }

    id = graphene.String(required=True)
    devices = graphene.List(
        DeviceInterface,
        required=True,
        device_type=graphene.String()
    )

    @staticmethod
    def build(data):
        return Board(id=data.get("board_id"), _data=data)

    @graphene.resolve_only_args
    def resolve_devices(self, device_type=None):
        return [self._type_map.get(d.get("device_type"), SensorDevice).build(d)
                for d in self._data.get("devices")]
