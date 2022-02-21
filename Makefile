help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:  ## Create a new environment with poetry and install with pre-commit hooks
	poetry install
	pre-commit install

test:  ## Run the test suite using pytest
	poetry run pytest --cov webapp

lint:  ## Run linting checks with flake8 and black
	poetry run flake8 src/
	poetry run black --check src/
	poetry run isort -c src/

format:  ## Run black to format the code
	poetry run black .
	poetry run isort src