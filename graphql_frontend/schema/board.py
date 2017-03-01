""" Board Schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene

from .device import Device, SystemDevice, SensorDevice


class Board(graphene.ObjectType):
    _data = None
    _type_map = {
        "system": SystemDevice
    }

    id = graphene.String(required=True)
    devices = graphene.List(Device, required=True)

    @staticmethod
    def build(data):
        return Board(id=data.get("board_id"), _data=data)

    def resolve_devices(self, args, context, info):
        return [self._type_map.get("device_type", SensorDevice).build(d)
                for d in self._data.get("devices")]
