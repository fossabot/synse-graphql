""" Cluster Schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import graphene

from .rack import Rack
from . import util


@util.resolve_assets
class Cluster(graphene.ObjectType):
    _routing = None  # Needed to build the racks list and saves a request
    _assets = [
        "hardware_version",
        "leader_service_profile",
        "model_number",
        "serial_number",
        "vendor"
    ]

    # Schema
    id = graphene.String(required=True)
    racks = graphene.List(
        lambda: Rack,
        required=True,
        id=graphene.String()
    )

    hardware_version = graphene.String(required=True)
    leader_service_profile = graphene.String(required=True)
    model_number = graphene.String(required=True)
    serial_number = graphene.String(required=True)
    vendor = graphene.String(required=True)

    @functools.lru_cache(maxsize=1)
    def _request_assets(self):
        return util.make_request(
            "asset/{0}".format(self.id)).get("cluster_info", {})

    @graphene.resolve_only_args
    def resolve_racks(self, id=None):
        def empty_id(x):
            return True

        def single_id(x):
            return x.get("rack_id") == id

        fn = empty_id
        if id is not None:
            fn = single_id

        return [Rack.build(r, self.id)
                for r in filter(fn, self._routing["racks"])]
