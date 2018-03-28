
VERSION = "2.0.5"

config = {
    'name': 'synse_graphql',
    'version': VERSION,
    'author': 'Thomas Rampelberg',
    'author_email': 'thomasr@vapor.io',
    'test_suite': 'nose.collector'
}

if __name__ == "__main__":
    from setuptools import setup

    setup(**config)
