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
    notifications = graphene.List(lambda: Notification, required=True)

    @graphene.resolve_only_args
    def resolve_clusters(self, id=None):
        def empty_id(x):
            return True

        def single_id(x):
            return x.get("cluster_id") == id

        fn = empty_id
        if id is not None:
            fn = single_id
        return [Cluster(id=c["cluster_id"], _routing=c)
                for c in filter(fn, util.make_request(
                    "routing_table").get("clusters", []))]

    def resolve_notifications(self, *args, **kwargs):
        return [Notification.build(d)
                for d in util.make_request(
                    "notifications").get("notifications", [])]
