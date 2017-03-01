""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene

from .cluster import Cluster
from .notification import Notification
from .device import SensorDevice, SystemDevice
from . import util


def create():
    return graphene.Schema(
        query=System,
        auto_camelcase=False,
        types=[
            SensorDevice,
            SystemDevice
        ]
    )


class System(graphene.ObjectType):
    clusters = graphene.List(lambda: Cluster, required=True)
    notifications = graphene.List(lambda: Notification, required=True)

    def resolve_clusters(self, args, context, info):
        return [Cluster(id=c["cluster_id"], _routing=c)
                for c in util.make_request(
                    "routing_table").get("clusters", [])]

    def resolve_notifications(self, *args, **kwargs):
        return [Notification.build(d)
                for d in util.make_request(
                    "notifications").get("notifications", [])]
