""" Board schema

    Author: Thomas Rampelberg
    Date:   2/27/2017
"""

import graphene

from . import util
from .device import Device, DeviceInterface


class Board(graphene.ObjectType):
    """Model for a Board, which contains Devices.
    """

    _data = None
    _parent = None

    id = graphene.String(required=True)
    devices = graphene.List(
        DeviceInterface,
        required=True,
        device_type=graphene.String()
    )

    @staticmethod
    def build(parent, data):
        """Build a new instance of a Board object.

        Args:
            parent (graphene.ObjectType): the parent object of the Board.
            data (dict): the data associated with the Board.

        Returns:
            Board: a new Board instance
        """
        return Board(_data=data, _parent=parent, **data)

    def resolve_devices(self, info, device_type=None):
        """Resolve all associated devices into their Device model.

        Args:
            device_type (str): the type of the device to filter for.

        Returns:
            list[Device]: a list of all resolved devices associated with this
                board.
        """
        return [Device.build(self, d)
                for d in util.arg_filter(
                    device_type,
                    lambda x: x.get('type') == device_type,
                    self._data.get('devices'))]
