""" Notification schema

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene


class NotificationSource(graphene.ObjectType):
    """ Model for the source of a Notification.
    """
    BoardID = graphene.String()
    DeviceID = graphene.String()
    DeviceType = graphene.String()
    Field = graphene.String()
    RackID = graphene.String()
    Reading = graphene.String()
    ZoneID = graphene.String()


class Notification(graphene.ObjectType):
    """ Model for a Notification.
    """
    _id = graphene.String(required=True)
    code = graphene.Int(required=True)
    resolved_on = graphene.String()
    severity = graphene.String(required=True)
    source = graphene.Field(NotificationSource, required=True)
    status = graphene.String(required=True)
    text = graphene.String(required=True)
    timestamp = graphene.String(required=True)

    @staticmethod
    def build(body):
        """ Build a new Notification object.

        Args:
            body (dict): the data for the notification.

        Returns:
            Notification: a new notification object.
        """
        return Notification(
            source=NotificationSource(**body.pop('source')), **body)
