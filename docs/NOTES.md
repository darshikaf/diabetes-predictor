## Design Decisions

### API Framework

* FastAPI was chosen mainly because of self documenting capability of the framework. In addition I've used dependency injection to allow customisations to response payload.

* Submodules were used for each endpoint type to enable scaling the system for new features such as mointoring, explainability etc.

<img src="FastAPI_module.png?raw=true" alt= “” width="400" height="400">

### `train` endpoint and model versioning

* `train` endpoint was implemented to support model retraining. This could mean either data refreshing or parameter tuning. 

* For the purpose of the coding test, `train` API is blocking. However for a production model it could be implemented as an async operation. It could also be implemented as its own microservice to remove integration with the scoring service.

* For the coding test, I have decided to store the model artifact ins the same container. For a production ready service, it could be implemented so that the model is stored in a artifact store, ex: S3, JFrog Artifactory etc.

* Model versioning is also very loosely enforced for the coding test. For a production system, I would use a model manifest to map to a model, that can be easily reproduced given the same training data and parameters.

### `score` endpoints

* Both `stream` and `batch` endpoints expects a post request with features in the body. Given the nature of the  feature data, I decided changing the payload signature for `stream` and `batch` adds unnecessary complexity.

* Input features are expected to be of type `list` to support adding new features to the payload for future versions of the model.

* For a production system, data would be read from a messaging queue for streaming or from database or batch processing. Depeding on the use case this system will require a db model and `sqlAlchemy` interface to read and write to a database.

* Use of a database will require setting up a migration strategy. Alembic can be used to codify db migrations and it can be set up as a pre-sync step of continous deployments.

* For batch processing it will need integration with a scheduler such as a cron job or a service like Airflow.


### Data Quality and Anomaly Detection

* For a production ready service, I would add functionality to compute data quality for scores. For batch scoring, data quality could be monitored using a population stability index. We will need to generate baseline data for PSI. 

* We will also need to implement a fallback strategy for when data quality of inferences fail. For ex: using a simple heuristic to replace the model score when QA fails.

### Security

* As the simplest security measure REST service can be deployed with SSL. In addition API authentication for endpoints can be implemented.


### CI/CD

* CI/CD is designed to comply with tagged releases. Committing to any branch will build, test and push a docker image. 
* When a release is published, a tagged image will be pushed. The way tagged releases are handled can be improved by investing more time on it. Ideally it should be done with re-usable github workflows to build, test and publish as a release image.
