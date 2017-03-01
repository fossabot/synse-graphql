""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene


class ChassisLocation(graphene.ObjectType):
    depth = graphene.String(required=True)
    horiz_pos = graphene.String(required=True)
    server_node = graphene.String(required=True)
    vert_pos = graphene.String(required=True)


class PhysicalLocation(graphene.ObjectType):
    depth = graphene.String(required=True)
    horizontal = graphene.String(required=True)
    vertical = graphene.String(required=True)


class Location(graphene.ObjectType):
    _data = None

    chassis_location = graphene.Field(ChassisLocation, required=True)
    physical_location = graphene.Field(PhysicalLocation, required=True)

    def resolve_chassis_location(self, *args, **kwargs):
        return ChassisLocation(**self._data.get("chassis_location"))

    def resolve_physical_location(self, *args, **kwargs):
        return PhysicalLocation(**self._data.get("physical_location"))


class Device(graphene.Interface):
    _data = None

    id = graphene.String(required=True)
    device_type = graphene.String(required=True)
    location = graphene.Field(Location, required=True)

    def resolve_location(self, *args, **kwargs):
        return Location(_data=self._data.get("location"))


class SensorDevice(graphene.ObjectType):
    _data = None

    class Meta:
        interfaces = (Device, )

    @staticmethod
    def build(data):
        return SensorDevice(
            id=data.get("device_id"),
            device_type=data.get("device_type"),
            _data=data
        )


class SystemDevice(graphene.ObjectType):
    _data = None

    class Meta:
        interfaces = (Device, )

    @staticmethod
    def build(data):
        return SystemDevice(
            id=data.get("device_id"),
            device_type=data.get("device_type"),
            _data=data
        )
