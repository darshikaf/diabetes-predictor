# diabetes-predictor

## Table of Contents

* [Docs](#docs)
* [Developing](#developing)
* [Tests](#tests)
* [Migration](#migration)
* [Release](#release)

## Docs

API docs can be accessed at `http://<ip-address>:8000/diabetes-predictor/docs#`.
## Developing

Develeopment workflow is as follows:

<img src="docs/development_workflow.png?raw=true" alt= “” width="400" height="100">

To contribute, first log in to ECR and make sure `AWS_ECR_AP_SE2` env variable is set.

Then build and run the service:

```bash
export VERSION=local
make run-local
```

* [`docker-compose.yml`](docker-compose.yml) file runs using `uvicorn` and mounts the code in the container so that updates to the code are reflected in the service automatically.

* For fast iterative development, you can also install this as a package:

```bash
conda create -n db_preds
python setup.py develop
```

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
### Pull Requests

* Committing to any branch will push a docker image to [Dockerhub](https://hub.docker.com/repository/docker/darshika/diabetes-predictor/general).

* To release to production, create and publish a release from github.
