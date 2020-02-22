#!/usr/bin/env bash
set -e -o pipefail

export PYTHONPATH=$PYTHONPATH:$(pwd)/turkology-annual-parser
VENV_DIR_TA=venv_ta_parser
PYTHON=$VENV_DIR_TA/bin/python
PIP=$VENV_DIR_TA/bin/pip
SOURCE_DIR=turkology-annual-parser
OCR_FILES=data/ocr/*
KEYWORDS_FILE=data/keywords.csv

venv() {
  if [[ ! -d $VENV_DIR_TA ]]; then
  echo "Initializing virtualenv in $VENV_DIR_TA/..."
  echo
    virtualenv $VENV_DIR_TA -p python3
  else
    echo "Virtualenv already exists at $VENV_DIR_TA, skipping initialization."
    echo "To start from a clean state, run ./go clean"
    echo
  fi
}

##DOC test: run all tests
goal_test() {
  ./go build && $PYTHON -m pytest
}

##DOC build: build the application
goal_build() {
  venv
  $PIP install -r requirements.txt
}

##DOC clean: remove virtual environment
goal_clean() {
  rm -rf $VENV_DIR_TA
}

##DOC run: run the application
goal_run() {
  venv
  echo "Starting..."
  $PYTHON $SOURCE_DIR/main.py --ocr-file $OCR_FILES --keyword-file $KEYWORDS_FILE \
  --find-authors \
  --resolve-repetitions
}

##DOC build-in-docker: build the application inside a docker container
goal_build-docker() {
  pip install --upgrade pip
  pip install -r requirements.txt
}

##DOC run-docker: run the application inside a docker container
goal_run-docker() {
  echo "Starting..."
  python $SOURCE_DIR/main.py --ocr-file $OCR_FILES --keyword-file $KEYWORDS_FILE \
  --find-authors \
  --resolve-repetitions
}


if type -t "goal_$1" &>/dev/null; then
  "goal_$1" "${@:2}"
else
  echo "usage: $0 <goal>"
  grep -e "^##DOC" <"$(basename "$0")" | sed "s/^##DOC \(.*\)/  \1/"
  exit 1
fi
