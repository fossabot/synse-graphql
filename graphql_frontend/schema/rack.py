""" Rack Schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import graphene

from . import util
from .board import Board


@util.resolve_assets
class Rack(graphene.ObjectType):
    _assets = [
        "failed_servers",
        "server_count"
    ]

    id = graphene.String(required=True)
    cluster_id = graphene.String(required=True)

    # routing table
    is_leader = graphene.Boolean(required=True)
    is_shadow = graphene.Boolean(required=True)
    vec_ip = graphene.String(required=True)

    # asset
    failed_servers = graphene.String(required=True)
    server_count = graphene.String(required=True)

    boards = graphene.List(lambda: Board, required=True)

    @functools.lru_cache(maxsize=1)
    def _request_assets(self):
        return util.make_request(
            "asset/{0}/{1}".format(self.cluster_id, self.id))

    def get_asset(self, asset, *args, **kwargs):
        return self._request_assets().get(asset, "")

    @staticmethod
    def build(info, cluster_id):
        _id = info["rack_id"]
        info.pop("rack_id")
        return Rack(id=_id, cluster_id=cluster_id, **info)

    def resolve_boards(self, *args, **kwargs):
        return [Board.build(b)
                for b in util.make_request(
                    "inventory/{0}/{1}".format(self.cluster_id, self.id)
                    ).get("clusters", [])[0].get("racks")[0].get("boards")]
