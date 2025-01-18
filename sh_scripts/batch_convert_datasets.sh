#!/bin/bash

# 実行用スクリプト

# 実行するスクリプトファイル名
EXEC_SCRIPT="./coco_to_pascal_dataset.sh"

# データセット番号の範囲
DATASET_NUMBERS=(1 2 3 4 5 6 7 8 9 10 11)

# データセットの種類
DATASET_TYPES=("test" "train" "val")

# すべてのデータセット番号と種類の組み合わせで実行
for DATASET_NO in "${DATASET_NUMBERS[@]}"; do
  for DATASET_TYPE in "${DATASET_TYPES[@]}"; do
    echo "Executing for dataset_${DATASET_NO}/$DATASET_TYPE"
    $EXEC_SCRIPT $DATASET_NO $DATASET_TYPE
  done
done
