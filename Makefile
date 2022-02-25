help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:  ## Create a new environment with poetry and install with pre-commit hooks
	poetry install
	pre-commit install

test:  ## Run the test suite using pytest
	poetry run pytest --cov webapp

lint:  ## Run linting checks with flake8 and black
	poetry run flake8 .
	poetry run black --check .
	poetry run isort -c .

format:  ## Run black to format the code
	poetry run black .
	poetry run isort .

local:  ## Run the webapp locally for debugging using Werkzeug
	poetry run python src/webapp/run.debug.py

docker-build:  ## Build the containerised webapp
	docker build -f Dockerfile -t "webapp:latest" .

docker-run:  ## Run the containerised application locally
	echo "Running at : http://localhost:5000/"
	docker run -ti --net=host --env-file ./.env "webapp:latest"

lambda-build:  ## Build the containerised application for AWS Lambda
	docker build -f Dockerfile.aws -t "webapp-lambda:latest" .

lambda-local:  ## Run the the containerised application for AWS Lambda locally
	docker run -ti -p 9000:8080 --env-file ./.env "webapp-lambda:latest" .

test-lambda:
	poetry run tests/test-lambda-local
