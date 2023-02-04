# diabetes-predictor

## Table of Contents

* [Developing](#developing)
* [Tests](#tests)
* [Migration](#migration)
* [Release](#release)

## Developing

Login to dockerhub.

Then build and run the service:

```bash
make run-local
```

The [`docker-compose.yml`](docker-compose.yml) file runs using `uvicorn` and mounts the code in the container so that updates to the code are reflected in the service automatically.

## Tests

### Style

Run this script to auto-fix styling:

```bash
make style-inplace
```

### Unit tests
```bash
make test-unit
```
### Integration tests

To run the integration tests locally:

```bash
make test-integration
```
