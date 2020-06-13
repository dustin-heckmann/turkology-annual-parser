#!/usr/bin/env bash
set -e -o pipefail

SOURCE_DIR=turkology-annual-parser
export PYTHONPATH=$PYTHONPATH:"$(pwd)/$SOURCE_DIR"
KEYWORDS_FILE=data/keywords.csv


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
  pipenv run mypy -p "$SOURCE_DIR"
}

##DOC build: build the application
goal_build() {
  pipenv install --dev
}

##DOC clean: remove virtual environment
goal_clean() {
  pipenv clean
}

##DOC run: run the application
goal_run() {
  echo "Starting..."
  pipenv run python $SOURCE_DIR/main.py \
  --find-authors \
  --resolve-repetitions \
  --input ta-data/ocr/* \
  --keyword-file ta-data/keywords.csv \
  --output ta-data/ta_citations.json \
  --zip-output ta-data/turkology_annual_export.zip
}

##DOC precommit: run build, lint, typecheck, test
goal_precommit() {
  goal_build
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
  pipenv run python $SOURCE_DIR/main.py \
  --input /ta-data/ocr/* \
  --keyword-file /ta-data/keywords.csv \
  --find-authors \
  --resolve-repetitions \
  --output /ta-data/ta_citations.json \
  --zip-output ta-data/turkology_annual_export.zip
}


if type -t "goal_$1" &>/dev/null; then
  "goal_$1" "${@:2}"
else
  echo "usage: $0 <goal>"
  grep -e "^##DOC" <"$(basename "$0")" | sed "s/^##DOC \(.*\)/  \1/"
  exit 1
fi
