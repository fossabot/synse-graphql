""" Rack schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene

from . import util
from .board import Board


class Rack(graphene.ObjectType):
    """ Model for the Rack object, which contains Boards.
    """
    _info = None
    _parent = None

    id = graphene.String(required=True)

    boards = graphene.List(
        lambda: Board,
        required=True,
        id=graphene.String())

    def get_boards(self):
        """ Get the boards associated with the Rack.

        Returns:
            list: a list of the associated Boards.
        """
        return self._info.get('boards')

    @staticmethod
    def build(parent, info):
        """ Build a new instance of a Rack object.

        Args:
            parent (graphene.ObjectType): the parent object of the Rack.
            info (dict): the data associated with the Rack.

        Returns:
            Rack: a new Rack instance
        """
        return Rack(_parent=parent, _info=info, **info)

    def resolve_boards(self, info, id=None):
        """ Resolve the Boards that are associated with the Rack.

        Args:
            id (str): the id of the board to filter for.

        Returns:
            list[Board]: a list of all resolved boards associated with this
                rack.
        """
        return [Board.build(self, b)
                for b in util.arg_filter(
                    id,
                    lambda x: x.get('id') == id,
                    self.get_boards())]
