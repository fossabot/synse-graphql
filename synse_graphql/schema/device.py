
""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017
"""
# pylint: disable=old-style-class,no-init

import functools

import graphene

from . import util


class DeviceReading(graphene.ObjectType):
    """ Model for data returned from Device readings
    """
    reading_type = graphene.String(required=True)
    value = graphene.String(required=True)


class DeviceInterface(graphene.Interface):
    """ Interface for all devices.
    """

    id = graphene.String(required=True)
    info = graphene.String(required=True)
    device_type = graphene.String(required=True)
    readings = graphene.List(DeviceReading)


class Device(graphene.ObjectType):
    """ Model for Devices, which contain DeviceReadings
    """

    _data = None
    _parent = None

    class Meta:
        interfaces = (DeviceInterface, )

    @classmethod
    def build(cls, parent, data):
        """ Build a new instance of the device.

        Args:
            parent: the parent object for the device.
            data: the data associated with the device to build.

        Returns:
            a new instance of the built device.
        """
        data['device_type'] = data.pop('type')
        return Device(_parent=parent, _data=data, **data)

    @property
    def backend(self):
        """ The backend this device is associated with. """
        return self._parent._parent.backend

    @property
    def rack_id(self):
        """ Get the rack id for the rack which the device resides on.
        """
        return self._parent._parent.id

    @property
    def board_id(self):
        """ Get the board id for the board which the device resides on.
        """
        return self._parent.id

    @property
    def _url(self):
        return 'read/{0}/{1}/{2}'.format(
            self.rack_id,
            self.board_id,
            self.id)

    @functools.lru_cache(maxsize=1)
    def _resolve_detail(self):
        """ Make a read request for the given device.
        """
        try:
            return util.make_request(self.backend, self._url).get('data')
        except Exception as e:
            pass

    def resolve_readings(self, *_):
        """ Build DeviceReading from _resolve_detail JSON
        """
        data = self._resolve_detail()
        if data:
            return [
                DeviceReading(
                    reading_type=d.get('type'), value=str(d.get('value')))
                for d in data if d is not None
            ]
