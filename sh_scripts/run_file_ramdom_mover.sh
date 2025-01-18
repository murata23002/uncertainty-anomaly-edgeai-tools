#!/bin/bash

# ベースディレクトリ設定
BASE_DIR="basedataset"

# 対象ディレクトリリスト
TARGET_DIRS=(
    "dataset"
)

# 移動割合設定 (train の 10% を val に移動)
RATIO=0.1

# Pythonスクリプトのパス
PYTHON_SCRIPT="random_file_mover.py"

# 各ディレクトリをループ処理
for TARGET in "${TARGET_DIRS[@]}"; do
    # train と val のパス設定
    SOURCE_DIRECTORY="${BASE_DIR}/${TARGET}/train"
    DESTINATION_DIRECTORY="${BASE_DIR}/${TARGET}/val"

    # ファイル数をカウント
    NUM_FILES=$(find "${SOURCE_DIRECTORY}/images" -type f | wc -l)
    MOVE_COUNT=$(echo "$NUM_FILES * $RATIO" | bc | awk '{print int($1)}') # 10%計算

    # val ディレクトリ作成 (必要な場合)
    mkdir -p "${DESTINATION_DIRECTORY}/images"
    mkdir -p "${DESTINATION_DIRECTORY}/annotations"

    # Pythonスクリプト実行
    echo "Processing: $TARGET (Moving $MOVE_COUNT files)"
    python3 "$PYTHON_SCRIPT" "$SOURCE_DIRECTORY" "$DESTINATION_DIRECTORY" "$MOVE_COUNT"

    # 完了メッセージ
    echo "Finished processing: $TARGET"
done

# 全体完了メッセージ
echo "All processing completed!"
