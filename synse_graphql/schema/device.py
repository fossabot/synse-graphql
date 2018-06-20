
""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017
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
        return util.make_request(self.backend, self._url)

    def _request_data(self, field, *_):
        """ Get the specified field from a device request response.

        Args:
            field: the field to extract from the request response.
        """
        result = self._resolve_detail().get('data').get(field).get('value')
        if result == 'null':
            raise Exception('Received null value - {}:{} {}'.format(
                self.device_type,
                field,
                self._url))
        return result


@resolve_fields
class AirflowDevice(DeviceBase):
    """ Model for a Airflow type device. """

    _resolve_fields = [
        'airflow'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    airflow = graphene.Float()


@resolve_fields
class PressureDevice(DeviceBase):
    """ Model for a DifferentialPressure type device. """

    _resolve_fields = [
        'pressure'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    pressure = graphene.Float()


@resolve_fields
class FanDevice(DeviceBase):
    """ Model for a fan type device.
    """

    _resolve_fields = [
        'fan_speed',
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    fan_speed = graphene.Int()


@resolve_fields
class HumidityDevice(DeviceBase):
    """ Model for a Humidity type device. """

    _resolve_fields = [
        'humidity'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    humidity = graphene.Float()


@resolve_fields
class LedDevice(DeviceBase):
    """ Model for an LED type device.
    """

    _resolve_fields = [
        'color',
        'state',
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    color = graphene.String()
    state = graphene.String()


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


@resolve_fields
class IdentityDevice(DeviceBase):
    """ Model for an Identity type device.
    """

    _resolve_fields = [
        'identity'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    identity = graphene.String()


@resolve_fields
class StatusDevice(DeviceBase):
    """ Model for a Status type device.
    """

    _resolve_fields = [
        'status'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    status = graphene.String()


@resolve_fields
class FrequencyDevice(DeviceBase):
    """ Model for a Frequency type device.
    """

    _resolve_fields = [
        'frequency'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    frequency = graphene.Float()


@resolve_fields
class VoltageDevice(DeviceBase):
    """ Model for a Voltage type device.
    """

    _resolve_fields = [
        'voltage'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    voltage = graphene.Float()


@resolve_fields
class CurrentDevice(DeviceBase):
    """ Model for a Current type device.
    """

    _resolve_fields = [
        'current'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    current = graphene.Float()


@resolve_fields
class PowerDevice(DeviceBase):
    """ Model for a Power type device.
    """

    _resolve_fields = [
        'power'
    ]

    class Meta:
        interfaces = (DeviceInterface, )

    power = graphene.Float()
