""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import itertools

import graphene

from . import util
from .device import Device
from .rack import Rack


def create():
    """Create a graphene schema for our graphql endpoints.

    Returns:
         graphene.Schema: the schema created for our graphql endpoints.
    """
    return graphene.Schema(
        query=Cluster,
        auto_camelcase=False,
        types=[Device, ]
    )


class Cluster(graphene.ObjectType):
    """Model for a cluster of racks.
    """

    # Schema
    racks = graphene.List(Rack, required=True, id=graphene.String())

    @functools.lru_cache(maxsize=1)
    def _request_assets(self):
        """Get the assets of the cluster.

        Returns:
            dict: a dictionary of assets mapped to empty strings.
        """
        return dict([(k, '') for k in self._assets])

    def resolve_racks(self, info, id=None):
        """Resolve the racks that belong to the cluster.

        Args:
            id (str): the id of the rack to filter upon.

        Returns:
            list[Rack]: a list of Rack objects that belong to the
                cluster.
        """
        return itertools.chain.from_iterable(
            [[
                Rack.build(self, backend, rack)
                for rack in util.arg_filter(
                    id, lambda x: x.get('id') == id, data.get('racks'))
            ] for backend, data in util.scan() if type(data) is dict]
        )
