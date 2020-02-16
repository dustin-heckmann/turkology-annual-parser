#!/usr/bin/env bash
set -e -o pipefail

export PYTHONPATH=$PYTHONPATH:$(pwd)/turkology-annual-parser

##DOC test: run all tests
goal_test() {
  ./go build && python -m pytest
}

##DOC build: build the application
goal_build() {
  pip install -r requirements.txt
}

##DOC run: run the application
goal_run() {
  ./go build && ./run.sh
}

if type -t "goal_$1" &>/dev/null; then
  "goal_$1" "${@:2}"
else
  echo "usage: $0 <goal>"
  grep -e "^##DOC" <"$(basename "$0")" | sed "s/^##DOC \(.*\)/  \1/"
  exit 1
fi
