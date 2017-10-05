# Kick the tires

```bash
make run
```

To stop it, you can run:

```bash
make down
```

At this point there is an interactive terminal running that you can do interactive queries with. Send your browser to `http://localhost:5001/graphql` and play around. Click the `Docs` tab on the right for the schema or go to `tests/queries/` to look at some example queries.

Note: the default configuration uses the embedded synse-server and ipmi emulator. If you'd like to use a different backend, check out `--help`.

# Development

## Run the server

```bash
make build dev
python runserver.py
```

- From outside the container (or inside it), you can run `curl localhost:5001`

## Use the query tool

```bash
make build dev
python runserver.py &
./query.py --list
./query.py test_racks
./query.py --help
```

## Run the tests (as part of development)

```
make build dev
tox
```

See [nosetests](http://nose.readthedocs.io/en/latest/usage.html) for some more examples. Adding `@attr('now')` to the top of a function is a really convenient way to just run a single test.

## Getting isort errors?

- See the changes:

```bash
isort graphql_frontend tests -rc -vb --dont-skip=__init_.py --diff
```

- Atomic updates:

```bash
isort graphql_frontend tests -rc -vb --dont-skip=__init_.py --atomic
```

# Testing (run the whole suite)

- Tests assume a running, emulated synse-server on the same host. It uses `localhost` to talk to the router. If this isn't where you're running it, change the config.
- `make test`
