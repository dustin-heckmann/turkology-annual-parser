#!/usr/bin/env bash

SOURCE_DIR=turkology-annual-parser
OCR_FILES=data/ocr/*.xml
KEYWORDS_FILE=data/keywords.csv

echo "Running..."
python $SOURCE_DIR/main.py --ocr-file $OCR_FILES --keyword-file $KEYWORDS_FILE \
  --find-authors \
   --resolve-repetitions \
