.PHONY: deps python-deps test test-django lint database help docs

###################################
### Dependency building

deps: python-deps

python-deps:  ## Install all dependencies, for running app, dev, and testing
	pip install -r requirements/frozen.txt
	pip install -r requirements/test.txt

vue-deps:  ## Install front-end dependencies
	cd ./vue && yarn install

###################################
### Testing

test: test-django lint  ## Run Django tests and flake8

test-django:  ## Run Django tests
	pytest

test-fast:  ## Run Django tests without search dependencies
	pytest -m "not solr"

lint:  ## Run flake8 over app
	flake8 orb

vue-test:  ## Run front-end JS tests
	cd ./vue && yarn run unit

vue-test-dev:  ## Run front-end JS tests
	cd ./vue && yarn run unit-dev

###################################
### Docker shortcuts

run:  ## Runs the dev containers
	docker-compose -f dev.yml up

build-docker:  ## Builds all available containers
	docker-compose -f dev.yml build

test-docker:  ## Runs tests in the Django container
	docker-compose -f dev.yml run django pytest

###################################
### Language
makemessages:  ## Make PO messages files
	./manage.py makemessages -l es -l pt_BR

register-languages:  ## Make migrations for new translated fields, migrate, and update fields
	./manage.py makemigrations
	./manage.py migrate
	./manage.py update_translation_fields

###################################
### Building project components

clean:  ## Removes extraneous files and build artifacts
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f &> /dev/null
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf &> /dev/null

build: python-deps node-deps database templates docs  ## Run all build commands, including dependencies, database, assets, and docs

docs:  ## Rebuild the documentation and open in default browser
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
	open docs/_build/html/index.html

database:  ## Migrate the database
	@echo "Setting up and updating the database..."
	./manage.py migrate --noinput

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

vue-dev: ## run vue compiler in dev version
	cd ./vue && yarn run dev

vue-build: ## run vue compiler for production
	cd ./vue && yarn run build
