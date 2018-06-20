""" Tests for the board schema

    Author: Kyler Burke
    Date:   6/19/2018

    \\//
     \/apor IO
"""

from nose.plugins.attrib import attr  # noqa

import synse_graphql.config
import synse_graphql.schema

from ..util import BaseSchemaTest


class TestBackend(BaseSchemaTest):
    """ Test creating schema with multiple backends, 1 of which is unreachable
    """

    def add_backends_to_config(self):
        """ Helper function to add backends to synse_grapqhl config
        """
        cfg_backends = [
            '--backend',
            'backend;;http://synse-server:5000',
            'backend-2;;http://synse-server-2:5000',
            'backend-3;;http://nonsynse-server:5000',
        ]
        synse_graphql.config.parse_args(cfg_backends)
        cfg = synse_graphql.config.options
        assert "backend" in cfg
        assert len(cfg["backend"]) == len(cfg_backends[1:])

    def test_cfg_parse(self):
        self.add_backends_to_config()

    def test_rack_backends(self):
        self.add_backends_to_config()
        racks = self.run_query("test_racks").get('data').get('racks')
        assert isinstance(racks, list)
        assert len(racks) == 2
        ids = [r.get("backend") for r in racks]
        assert set(ids) == set(["backend", "backend-2"])
