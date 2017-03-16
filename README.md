# graphql-frontend

## Development

### Run the server

1. `make dev`
2. `python runserver.py`
3. (outside the container) `http localhost:5001`

### Run the tests

1. `make dev`
2. `make one test=

### Getting isort errors?

- See the changes: `isort graphql_frontend tests -rc -vb --dont-skip=__init_.py --diff`
- Atomic updates: `isort graphql_frontend tests -rc -vb --dont-skip=__init_.py --atomic`

## Testing

- `make test`
