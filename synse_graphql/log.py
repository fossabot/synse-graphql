import json
import logging.config
import os


def setup_logging(name='logging.json'):
    path = os.path.join(os.path.dirname(__file__), '..', name)
    with open(path, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)
