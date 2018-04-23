import logging
import logging.config
import sys


def setup_logging(cfg=None):
    if not cfg:
        cfg = LOGGING
    logging.config.dictConfig(cfg)


LOGGING = dict(
    version=1,
    disable_existing_loggers=False,

    formatters={
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
            'class': 'logging.Formatter'
        },
    },
    handlers={
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
    },
    loggers={
        '': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': True
        },
    }
)
