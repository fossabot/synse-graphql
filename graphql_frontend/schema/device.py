""" Device schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene


class Device(graphene.Interface):
    id = graphene.String(required=True)
    type = graphene.String(required=True)


class SensorDevice(graphene.ObjectType):
    class Meta:
        interfaces = (Device, )


class SystemDevice(graphene.ObjectType):
    class Meta:
        interfaces = (Device, )
