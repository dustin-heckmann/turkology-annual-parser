#!/usr/bin/env bash

# This script contains all tasks related to building, testing and running the application

## Adding a new task:
# 1. To add a task named 'example', implement it as a function named 'goal_example()'
# 2. Above the function name, add a usage hint, e.g. '##DOC: example: this is an example'
#    -> Usage hints will be displayed when running this script without any argument or with an unknown argument
# 3. The task can now be run with `./go example`


set -e -o pipefail
BASE_DIR="$(dirname $0)"
SOURCE_DIR="$BASE_DIR/turkology-annual-parser"

## Tasks  ================================================================================
##DOC test: run all tests
goal_test() {
  pipenv run pytest -vv
}

##DOC lint: run linter
goal_lint() {
  pipenv run flake8 "$SOURCE_DIR"
}

##DOC typecheck: run typecheck (using mypy)
goal_typecheck() {
  pipenv run mypy -p $(basename "$SOURCE_DIR")
}

##DOC build: build the application
goal_build() {
  pipenv install --dev
}

##DOC clean: remove virtual environment
goal_clean() {
  pipenv --rm
}

##DOC run: run the application
goal_run() {
  DATA_DIR=${1:-"$BASE_DIR/ta-data"}
  echo "Starting..."
  pipenv run python $SOURCE_DIR/main.py \
  --find-authors \
  --resolve-repetitions \
  --input "$DATA_DIR"/ocr/* \
  --keyword-file "$DATA_DIR/keywords.csv" \
  --output "$DATA_DIR/ta_citations.json" \
  --zip-output "$DATA_DIR/turkology_annual_export.zip"
}

##DOC precommit: run build, lint, typecheck, test
goal_precommit() {
  goal_lint
  goal_typecheck
  goal_test
}

##DOC build-docker: build the application inside a docker container
goal_build-docker() {
  pip install --upgrade pip
  pip install pipenv
  pipenv install
}

##DOC run-docker: run the application inside a docker container
goal_run-docker() {
  goal_run "/ta-data"
}
## ========================================================================================

## Include go.helpers script which invokes specified task or prints usage hint
source "$BASE_DIR/go.helpers"
