## Design Decisions

### API Framework

* `FastAPI` was chosen mainly because of its high performance compared to `Flask` and self documenting capability of the framework. In addition I've used dependency injection to allow customisations to response payload.

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

* A kill switch that can be triggered when n number of poor quality scores are generated can be implemented to stop poor data from going downstream. Alarms and notifications can be integrated to triage the scenario to model owners.

### Security

* As the simplest security measure REST service can be deployed with SSL. In addition API authentication for endpoints can be implemented.

* Authentication method for AWS should be updated to use an assumed role for improved security. 


### CI/CD

* CI/CD is designed to comply with tagged releases. Committing to any branch will build, test and push a docker image. 
* When a release is published, a tagged image will be pushed. The way tagged releases are handled can be improved by investing more time on it. Ideally it should be done with re-usable github workflows to build, test and publish as a release image.
* Due to time constraints, Continous Deployment is implememnted to tag every new commit as latest and deployed to ECS. For production ready environment, it could be implemented with a tool like ArgoCD. Alternatively FastAPI application can be directly deployed to AWS Serverless.

### Monitoring on service

* In a production environment, it is critical to ensure high availability. A part of high availability will be addressed by the ochestration platform (in case kubernetes or a similar platform is used). To ensure application health, network and server monitoring with tools like Nagios can be used. Alternatively, logging tools come with its own Event Definitions and notifications on those events -- which can be used to raise alerts when application is unhealthy.

### AWS Env variables and Authentication

* Locally building and running the container should not require authentication. However `AWS_ECR_AP_SE2` will be required. Value for this secret is shared in the email.
