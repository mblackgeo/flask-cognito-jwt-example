help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:  ## Create a new environment with poetry and install with pre-commit hooks
	poetry install
	pre-commit install

test:  ## Run the test suite using pytest
	poetry run pytest --cov webapp

lint:  ## Run linting checks with flake8, isort, and black
	poetry run flake8 .
	poetry run black --check .
	poetry run isort -c .

format:  ## Run black and isort to format the code
	poetry run black .
	poetry run isort .

local:  ## Run the webapp locally for debugging using Werkzeug
	poetry run python src/webapp/lambda.py

docker-build:  ## Build the containerised webapp
	docker build -f Dockerfile -t "webapp:latest" .

docker-run:  ## Run the containerised application locally
	echo "Running at : http://localhost:5000/"
	docker run -ti --net=host --env-file ./.env "webapp:latest"
