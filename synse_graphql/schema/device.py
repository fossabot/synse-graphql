
""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""
# pylint: disable=old-style-class,no-init

import functools

import graphene

from . import util


def resolve_fields(cls):
    """Class decorator to set the _resolve_fields member values
    as methods onto the class.

    Args:
        cls: the class being decorated.

    Returns:
        the class with new attributes assigned.
    """
    for field in cls._resolve_fields:
        setattr(
            cls,
            'resolve_{0}'.format(field),
            functools.partialmethod(cls._request_data, field))
    return cls


class DeviceInterface(graphene.Interface):
    """ Interface for all devices.
    """

    id = graphene.String(required=True)
    info = graphene.String(required=True)
    device_type = graphene.String(required=True)


class DeviceBase(graphene.ObjectType):
    """ Base class for all devices.
    """

    _data = None
    _parent = None
    _root = None

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
        return globals().get(cls.__name__)(
            _parent=parent,
            _data=data,
            **data,
        )

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

    @functools.lru_cache(maxsize=1)
    def _resolve_detail(self):
        """ Make a read request for the given device.
        """
        print(util.make_request('read/{0}/{1}/{2}'.format(
            self.rack_id,
            self.board_id,
            self.id)))
        return util.make_request('read/{0}/{1}/{2}'.format(
            self.rack_id,
            self.board_id,
            self.id))

    def _request_data(self, field, *_):
        """ Get the specified field from a device request response.

        Args:
            field: the field to extract from the request response.
        """
        return self._resolve_detail().get('data').get(field).get('value')


@resolve_fields
class AirflowDevice(DeviceBase):
    """ Model for a Airflow type device. """

    _resolve_fields = [
        'airflow'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    airflow = graphene.Float(required=True)


@resolve_fields
class DifferentialPressureDevice(DeviceBase):
    """ Model for a DifferentialPressure type device. """

    _resolve_fields = [
        'pressure'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    pressure = graphene.Float(required=True)


@resolve_fields
class FanDevice(DeviceBase):
    """ Model for a fan type device.
    """

    _resolve_fields = [
        'fan_speed',
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    fan_speed = graphene.Int(required=True)


@resolve_fields
class HumidityDevice(DeviceBase):
    """ Model for a Humidity type device. """

    _resolve_fields = [
        'humidity'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    humidity = graphene.Float(required=True)


@resolve_fields
class LedDevice(DeviceBase):
    """ Model for an LED type device.
    """

    _resolve_fields = [
        'blink',
        'color',
        'state',
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    blink = graphene.String(required=True)
    color = graphene.String(required=True)
    state = graphene.String(required=True)


@resolve_fields
class TemperatureDevice(DeviceBase):
    """ Model for a temperature type device.
    """

    _resolve_fields = [
        'temperature'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    temperature = graphene.Float()
