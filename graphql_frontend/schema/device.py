""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import graphene

from . import util


def setup_resolve(cls):
    for field, field_cls in cls._fields:
        setattr(
            cls,
            "resolve_{0}".format(field),
            functools.partialmethod(resolve_class, field, field_cls)
        )
    return cls


def resolve_class(self, field, cls, *args, **kwargs):
    return cls(**self._data.get(field))


class ChassisLocation(graphene.ObjectType):
    depth = graphene.String(required=True)
    horiz_pos = graphene.String(required=True)
    server_node = graphene.String(required=True)
    vert_pos = graphene.String(required=True)


class PhysicalLocation(graphene.ObjectType):
    depth = graphene.String(required=True)
    horizontal = graphene.String(required=True)
    vertical = graphene.String(required=True)


@setup_resolve
class Location(graphene.ObjectType):
    _data = None
    _fields = [
        ("chassis_location", ChassisLocation),
        ("physical_location", PhysicalLocation)
    ]

    chassis_location = graphene.Field(ChassisLocation, required=True)
    physical_location = graphene.Field(PhysicalLocation, required=True)


class DeviceInterface(graphene.Interface):
    _data = None

    id = graphene.String(required=True)
    device_type = graphene.String(required=True)
    location = graphene.Field(Location, required=True)

    def resolve_location(self, *args, **kwargs):
        return Location(_data=self._data.get("location"))


class BaseDevice(graphene.ObjectType):
    _data = None
    _parent = None

    @classmethod
    def build(cls, parent, data):
        return globals().get(cls.__name__)(
            id=data.get("device_id"),
            device_type=data.get("device_type"),
            _parent=parent,
            _data=data
        )

    @property
    def cluster_id(self):
        return self._parent._parent._parent.id

    @property
    def rack_id(self):
        return self._parent._parent.id

    @property
    def board_id(self):
        return self._parent.id


class SensorDevice(BaseDevice):
    class Meta:
        interfaces = (DeviceInterface, )


# thomasr: need to implement all the device types
# 'pressure', 'vapor_fan', 'temperature', 'power', 'fan_speed',
# 'vapor_rectifier', 'vapor_led', 'vapor_battery', 'led', 'system'
class PressureDevice(BaseDevice):
    class Meta:
        interfaces = (DeviceInterface, )

    pressure_kpa = graphene.String(required=True)

    def resolve_pressure_kpa(self, *args, **kwargs):
        return util.make_request("read/{0}/{1}/{2}/{3}/{4}".format(
            self.cluster_id,
            self.rack_id,
            self.device_type,
            self.board_id,
            self.id)).get("pressure_kpa")


class BoardInfo(graphene.ObjectType):
    manufacturer = graphene.String(required=True)
    part_number = graphene.String(required=True)
    product_name = graphene.String(required=True)
    serial_number = graphene.String(required=True)


class ChassisInfo(graphene.ObjectType):
    chassis_type = graphene.String(required=True)
    part_number = graphene.String(required=True)
    serial_number = graphene.String(required=True)


class ProductInfo(graphene.ObjectType):
    asset_tag = graphene.String(required=True)
    manufacturer = graphene.String(required=True)
    part_number = graphene.String(required=True)
    product_name = graphene.String(required=True)
    serial_number = graphene.String(required=True)
    version = graphene.String(required=True)


@setup_resolve
class Asset(graphene.ObjectType):
    _data = None
    _fields = [
        ("board_info", BoardInfo),
        ("chassis_info", ChassisInfo),
        ("product_info", ProductInfo)
    ]

    board_info = graphene.Field(BoardInfo, required=True)
    chassis_info = graphene.Field(ChassisInfo, required=True)
    product_info = graphene.Field(ProductInfo, required=True)


class SystemDevice(graphene.ObjectType):
    _data = None

    class Meta:
        interfaces = (DeviceInterface, )

    hostnames = graphene.List(graphene.String, required=True)
    ip_addresses = graphene.List(graphene.String, required=True)
    asset = graphene.Field(Asset, required=True)

    @staticmethod
    def build(data):
        return SystemDevice(
            id=data.get("device_id"),
            device_type=data.get("device_type"),
            _data=data
        )

    def resolve_hostnames(self, *args, **kwargs):
        return self._data.get("hostnames")

    def resolve_ip_addresses(self, *args, **kwargs):
        return self._data.get("ip_addresses")

    def resolve_asset(self, *args, **kwargs):
        return Asset(_data=self._data.get("asset"))
