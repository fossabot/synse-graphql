""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene

from .cluster import Cluster
from .notification import Notification
from .device import SensorDevice, SystemDevice, PressureDevice
from . import util


def create():
    return graphene.Schema(
        query=System,
        auto_camelcase=False,
        types=[
            SensorDevice,
            SystemDevice,
            PressureDevice
        ]
    )


class System(graphene.ObjectType):
    clusters = graphene.List(
        lambda: Cluster,
        required=True,
        id=graphene.String()
    )
    notifications = graphene.List(
        lambda: Notification,
        required=True,
        _id=graphene.String()
    )

    @graphene.resolve_only_args
    def resolve_clusters(self, id=None):
        return [Cluster(id=c["cluster_id"], _routing=c)
                for c in util.arg_filter(
                    id,
                    lambda x: x.get("cluster_id") == id,
                    util.make_request(
                        "routing_table").get("clusters", []))]

    @graphene.resolve_only_args
    def resolve_notifications(self, _id=None):
        return [Notification.build(d)
                for d in util.arg_filter(
                    _id,
                    lambda x: x.get("_id") == _id,
                    util.make_request(
                        "notifications").get("notifications", []))]
