""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import functools
import graphene
import graphene.types.datetime
import requests
import requests.compat

BASE_URL = "http://172.17.0.1:4998/vaporcore/1.0/routing/"
SESSION = requests.Session()

# AUTH
AUTH_USERNAME = "admin"
AUTH_PASSWORD = "Vapor"


def login():
    # thomasr: need some logging here for success/failure
    SESSION.post(requests.compat.urljoin(BASE_URL, "login"), data={
        "username": AUTH_USERNAME,
        "password": AUTH_PASSWORD,
        "target": "",
        "redirect_target": ""
    }, allow_redirects=False)


def make_request(url):
    result = SESSION.get(requests.compat.urljoin(BASE_URL, url))
    if result.status_code == 401:
        login()
        return make_request(url)
    return result.json()


def get_asset(self, asset, *args, **kwargs):
    """Fetch the value for a specific asset.

    Gets converted into resolve_asset_name(). See _assets for the list that
    are using this method as resolve.
    """
    return self._request_assets().get(asset, "")


def resolve_assets(cls):
    """Decorator to dynamically resolve fields.

    Add resolve methods for everything in _assets.
    """
    for asset in cls._assets:
        setattr(
            cls,
            "resolve_{0}".format(asset),
            functools.partialmethod(get_asset, asset))
    return cls


@resolve_assets
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

    @functools.lru_cache(maxsize=1)
    def _request_assets(self):
        return make_request(
            "asset/{0}/{1}".format(self.cluster_id, self.id))

    def get_asset(self, asset, *args, **kwargs):
        return self._request_assets().get(asset, "")

    @staticmethod
    def build(info, cluster_id):
        _id = info["rack_id"]
        info.pop("rack_id")
        return Rack(id=_id, cluster_id=cluster_id, **info)


@resolve_assets
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
    racks = graphene.List(lambda: Rack, required=True)

    hardware_version = graphene.String(required=True)
    leader_service_profile = graphene.String(required=True)
    model_number = graphene.String(required=True)
    serial_number = graphene.String(required=True)
    vendor = graphene.String(required=True)

    @functools.lru_cache(maxsize=1)
    def _request_assets(self):
        return make_request(
            "asset/{0}".format(self.id)).get("cluster_info", {})

    def resolve_racks(self, args, context, info):
        return [Rack.build(r, self.id) for r in self._routing["racks"]]


class NotificationSource(graphene.ObjectType):
    BoardID = graphene.String()
    DeviceID = graphene.String(required=True)
    DeviceType = graphene.String(required=True)
    Field = graphene.String(required=True)
    RackID = graphene.String()
    Reading = graphene.String(required=True)
    ZoneID = graphene.String(required=True)


class Notification(graphene.ObjectType):
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
        return Notification(
            source=NotificationSource(**body.pop("source")), **body)


class System(graphene.ObjectType):
    clusters = graphene.List(lambda: Cluster, required=True)
    notifications = graphene.List(lambda: Notification, required=True)

    def resolve_clusters(self, args, context, info):
        return [Cluster(id=c["cluster_id"], _routing=c)
                for c in make_request("routing_table").get("clusters", [])]

    def resolve_notifications(self, *args, **kwargs):
        return [Notification.build(d)
                for d in make_request(
                    "notifications").get("notifications", [])]


schema = graphene.Schema(
    query=System,
    auto_camelcase=False)

# Example query
# pprint.pprint(schema.schema.execute("{ notifications { _id source { ZoneID } } clusters { id hardware_version racks { id   is_leader } } }").data)
