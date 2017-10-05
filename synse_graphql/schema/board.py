""" Board schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
import inflection

from . import device, util


class Board(graphene.ObjectType):
    """Model for a Board, which contains Devices.
    """

    _data = None
    _parent = None

    id = graphene.String(required=True)
    devices = graphene.List(
        device.DeviceInterface,
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
        return Board(id=data.get('board_id'), _data=data, _parent=parent)

    @staticmethod
    def device_class(device_type):
        """Get the device class for the given device type.

        Args:
            device_type (str): the name of the device type to get the
                device class for.

        Returns:
            the device class, as defined in the `devices` module.
        """
        return getattr(
            device,
            '{0}Device'.format(inflection.camelize(device_type)),
            device.SensorDevice)

    @graphene.resolve_only_args
    def resolve_devices(self, device_type=None):
        """Resolve all associated devices into their Device model.

        Args:
            device_type (str): the type of the device to filter for.

        Returns:
            list[Device]: a list of all resolved devices associated with this
                board.
        """
        return [self.device_class(d.get('device_type')).build(self, d)
                for d in util.arg_filter(
                    device_type,
                    lambda x: x.get('device_type') == device_type,
                    self._data.get('devices'))]
