""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
import requests
import requests.compat

BASE_URL = "http://172.18.0.1:4998/vaporcore/1.0/routing/"


def make_request(url):
    return requests.get(requests.compat.urljoin(BASE_URL, url)).json()


class Rack(graphene.ObjectType):
    id = graphene.String(required=True)
    is_leader = graphene.Boolean(required=True)
    is_shadow = graphene.Boolean(required=True)
    vec_ip = graphene.String(required=True)


class Cluster(graphene.ObjectType):
    # Private Vars
    _routing = None  # Needed to build the racks list and saves a request

    # Schema
    id = graphene.String(required=True)
    racks = graphene.List(lambda: Rack, required=True)

    def build_rack(self, routing_info):
        _id = routing_info["rack_id"]
        routing_info.pop("rack_id")
        return Rack(id=_id, **routing_info)

    def resolve_racks(self, args, context, info):
        return [self.build_rack(r) for r in self._routing["racks"]]


class System(graphene.ObjectType):
    clusters = graphene.List(lambda: Cluster, required=True)

    def resolve_clusters(self, args, context, info):
        routing_table = make_request("routing_table")["clusters"]
        return [Cluster(id=c["cluster_id"], _routing=c)
                for c in routing_table]


schema = graphene.Schema(
    query=System,
    auto_camelcase=False)

# Example query
# pprint.pprint(
#     schema.schema.execute("{ clusters { id racks { id is_leader } } }").data)
