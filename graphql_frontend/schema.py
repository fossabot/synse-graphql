""" Schema for GraphQL

    Author: Thomas Rampelberg
    Date:   2/27/2017

    \\//
     \/apor IO
"""

import graphene
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


class Rack(graphene.ObjectType):
    id = graphene.String(required=True)
    cluster_id = graphene.String(required=True)

    # routing table
    is_leader = graphene.Boolean(required=True)
    is_shadow = graphene.Boolean(required=True)
    vec_ip = graphene.String(required=True)

    # asset
    failed_servers = graphene.String(required=True)
    server_count = graphene.String(required=True)

    @staticmethod
    def build(info, cluster_id):
        _id = info["rack_id"]
        info.pop("rack_id")
        return Rack(
            id=_id,
            cluster_id=cluster_id,
            **info,
            **Rack.get_assets(_id, cluster_id))

    @staticmethod
    def get_assets(_id, cluster_id):
        assets = make_request("asset/{0}/{1}".format(cluster_id, _id))
        return {k: v for k, v in assets.items()
                if k in ("failed_servers", "server_count")}


class Cluster(graphene.ObjectType):
    # Private Vars
    _routing = None  # Needed to build the racks list and saves a request

    # Schema
    id = graphene.String(required=True)
    racks = graphene.List(lambda: Rack, required=True)

    hardware_version = graphene.String(
        name='hardware_version', required=True)
    leader_service_profile = graphene.String(required=True)
    model_number = graphene.String(required=True)
    serial_number = graphene.String(required=True)
    vendor = graphene.String(required=True)

    @staticmethod
    def build(_id, _routing):
        return Cluster(
            id=_id,
            _routing=_routing,
            **Cluster.get_assets(_id))

    @staticmethod
    def get_assets(_id):
        assets = make_request("asset/{0}".format(_id)).get("cluster_info", {})
        assets.pop("cluster_id")
        return assets

    def resolve_racks(self, args, context, info):
        return [Rack.build(r, self.id) for r in self._routing["racks"]]


class System(graphene.ObjectType):
    clusters = graphene.List(lambda: Cluster, required=True)

    def resolve_clusters(self, args, context, info):
        try:
            return [Cluster.build(c["cluster_id"], c)
                    for c in make_request("routing_table")["clusters"]]
        except Exception as e:
            print(e)


schema = graphene.Schema(
    query=System,
    auto_camelcase=False)

# Example query
# pprint.pprint(schema.schema.execute("{ clusters { id hardware_version racks { id failed_servers is_leader } } }").data)
