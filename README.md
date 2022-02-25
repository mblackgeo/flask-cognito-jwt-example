# Flask - AWS Cognito integration example

The example web application uses [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [AWS Cognito](https://aws.amazon.com/cognito/) with [JSON Web Tokens (JWT)](https://jwt.io/) to protect specific pages. This is built on [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) and [Flask-AWSCognito](https://flask-awscognito.readthedocs.io/en/latest/index.html) to assist with the handling of JWTs to protect specific routes. It was inspired by the blog post [Integrating Cognito with Flask](https://medium.com/analytics-vidhya/integrating-cognito-with-flask-e00010866054) by Martin Campbell.

## Getting started

Prequisites:

* [poetry](https://python-poetry.org/)
* [pre-commit](https://pre-commit.com/)
* [AWS CDK](https://aws.amazon.com/cdk/) version 2.13.0

Setup as follows:

```shell
# setup the python environment with poetry
make install

# deploy the infra (Cognito, API Gateway, Lambda)
cd deploy
cdk deploy --all

# Populate the .env file with CDK outputs
cp .env.example .env
vi .env

# run locally using Workzeug
make local  # or go to the AWS API Gateway URL

# check other useful commands
make help
```

The Makefile includes helpful commands setting a development environment, get started by installing the package into a new environment and setting up pre-commit by running `make install`. Run `make help` to see additional available commands (e.g. linting, testing, docker, and so on).


The application can be run locally through docker (`make docker-build && make docker-run`) or installed to a virtualenv using poetry and the `src/webapp/run.debug.py` (for debugging) or the `src/webapp/run.bjoern.py` for the production WSGI server (see Development below for more details). The app should be launched at [http://localhost:5000](http://localhost:5000) and a login link should redirect you to the hosted Cognito UI to sign up / sign in. Once logged in, a cookie will be set to save the JWT and you will be redirected to the [private page](http://localhost:5000/private). You may also view details of the JWT at the [`/token`](http://localhost:5000/token) endpoint.


## Development

* [Pytest](https://docs.pytest.org/en/6.2.x/) is used for the functional tests of the application (see `/tests`).
* Code is linted using [flake8](https://flake8.pycqa.org/en/latest/)
* Code formatting is validated using [Black](https://github.com/psf/black)
* [pre-commit](https://pre-commit.com/) is used to run these checks locally before files are pushed to git
* The [Github Actions pipeline](.github/workflows/pipeline.yml) also runs these checks and tests


## TODO

- [x] CORS
- [ ] Serverless deployment with [AWS CDK](https://aws.amazon.com/cdk/) [in progress]
- [ ] Is [CSRF protection](https://flask-jwt-extended.readthedocs.io/en/stable/options/#cross-site-request-forgery-options) required?