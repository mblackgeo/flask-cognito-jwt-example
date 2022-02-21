# Flask - Cognito integration

The example web application uses [Flask](https://flask.palletsprojects.com/en/2.0.x/) [AWS Cognito](https://aws.amazon.com/cognito/).

TODO detailed explanation and diagrams.

## Development

Prequisites:

* [poetry](https://python-poetry.org/)
* [pre-commit](https://pre-commit.com/)

The Makefile includes helpful commands setting a development environment, get started by installing the package into a new environment and setting up pre-commit by running make install. Run make help to see additional available commands (e.g. linting, testing, docker, and so on).

* [Pytest](https://docs.pytest.org/en/6.2.x/) is used for the functional tests of the application (see `/tests`).
* Code is linted using [flake8](https://flake8.pycqa.org/en/latest/)
* Code formatting is validated using [Black](https://github.com/psf/black)
* [pre-commit](https://pre-commit.com/) is used to run these checks locally before files are pushed to git
* The [Github Actions pipeline](.github/workflows/pipeline.yml) also runs these checks and tests

## Deployment

Deployment to AWS is handled by the AWS Cloud Development Kit (CDK). All code is in [`/infra`](/infra).


## Useful resources

* [Integrating Cognito with Flask](https://medium.com/analytics-vidhya/integrating-cognito-with-flask-e00010866054)