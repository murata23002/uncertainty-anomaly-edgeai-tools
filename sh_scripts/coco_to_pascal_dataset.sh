#!/bin/bash

# 共通部分の定義
SCRIPT="dataset_converter.py"
CONVERSION_TYPE="coco_to_pascal"
BASE_DATASET_DIR=""
ANNOTATION_DIR="annotations/annotations.json"
OUTPUT_BASE_DIR="./dist"

TEST="test"
TRAIN="train"
VAL="val"

# 引数を受け取る（例: 1, 2, 3 などの番号と test, train, val）
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 {1|2|3...} {test|train|val}"
  exit 1
fi

# 引数を使ってパスを組み立てる
DATASET_NO=$1
DATASET_TYPE=$2

# 組み立てたパス
ANNOTATION_PATH="${BASE_DATASET_DIR}_${DATASET_NO}/${DATASET_TYPE}/${ANNOTATION_DIR}"
OUTPUT_PATH="${OUTPUT_BASE_DIR}/dataset_${DATASET_NO}/${DATASET_TYPE}"

echo $ANNOTATION_PATH
echo $OUTPUT_PATH
# 実行
python $SCRIPT $CONVERSION_TYPE $ANNOTATION_PATH $OUTPUT_PATH
