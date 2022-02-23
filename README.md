# Flask - AWS Cognito integration example

The example web application uses [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [AWS Cognito](https://aws.amazon.com/cognito/) with [JSON Web Tokens (JWT)](https://jwt.io/) to protect specific pages. This is built on [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) and [Flask-AWSCognito](https://flask-awscognito.readthedocs.io/en/latest/index.html) to assist with the handling of JWTs to protect specific routes. It was inspired by the blog post [Integrating Cognito with Flask](https://medium.com/analytics-vidhya/integrating-cognito-with-flask-e00010866054) by Martin Campbell.

## Getting started

To get started, setup a [Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-user-pool.html) in AWS:

* At Step 5 of setup (Integrate your app), ensure to check the box for the "Use the Cognito Hosted UI"
* When creating your "Initial app client", check the radio button to "Generate a client secret"
* Set "Allowed callback URLs" to your site URL (e.g. `http://<FLASK_SITE_URL>/postlogin`), for example: `http://localhost:5000/postlogin`

After setting up the user pool, create a `.env` file (following `.env.example`) and populate the parameters from your newly created user pool:

```shell
FLASK_APP=webapp
FLASK_ENV=dev
FLASK_SITE_URL=http://localhost:5000

# AWS account and region used for deployment (or where Cognito is running)
AWS_ACCOUNT=
AWS_REGION=

# These are required if running locally, when deploying with CDK they will
# be automatically populated in the running container in AWS Lambda
AWS_COGNITO_DOMAIN=
AWS_COGNITO_USER_POOL_ID=
AWS_COGNITO_USER_POOL_CLIENT_ID=
AWS_COGNITO_USER_POOL_CLIENT_SECRET=

# optional, set to deploy to a custom URL: <api_subdomain.domain_name>
# Must have the domain registered in Route 53 already
AWS_DOMAIN_NAME=
AWS_API_SUBDOMAIN=
AWS_COGNITO_SUBDOMAIN=auth  # set a custom subdomain for Cognito
```

The application can be run locally through docker (`make docker-build && make docker-run`) or installed to a virtualenv using poetry and the `src/webapp/run.debug.py` (for debugging) or the `src/webapp/run.bjoern.py` for the production WSGI server (see Development below for more details). The app should be launched at [http://localhost:5000](http://localhost:5000) and a login link should redirect you to the hosted Cognito UI to sign up / sign in. Once logged in, a cookie will be set to save the JWT and you will be redirected to the [private page](http://localhost:5000/private). You may also view details of the JWT at the [`/token`](http://localhost:5000/token) endpoint.

## Development

Prequisites:

* [poetry](https://python-poetry.org/)
* [pre-commit](https://pre-commit.com/)
* A [Cognito User Pool](https://aws.amazon.com/cognito/)
* A populated `.env` file (based on `.env.example`), see "Getting Started" above for more details

The Makefile includes helpful commands setting a development environment, get started by installing the package into a new environment and setting up pre-commit by running `make install`. Run `make help` to see additional available commands (e.g. linting, testing, docker, and so on).

* [Pytest](https://docs.pytest.org/en/6.2.x/) is used for the functional tests of the application (see `/tests`).
* Code is linted using [flake8](https://flake8.pycqa.org/en/latest/)
* Code formatting is validated using [Black](https://github.com/psf/black)
* [pre-commit](https://pre-commit.com/) is used to run these checks locally before files are pushed to git
* The [Github Actions pipeline](.github/workflows/pipeline.yml) also runs these checks and tests

## Deployment

* CDK version 2.13.0
* Use CDK to create the required resources (Cognito, Lambda, API Gateway)

TODO - more detail

## TODO

- [x] CORS
- [ ] [CSRF protection](https://flask-jwt-extended.readthedocs.io/en/stable/options/#cross-site-request-forgery-options)
- [ ] Serverless deployment with [AWS CDK](https://aws.amazon.com/cdk/)