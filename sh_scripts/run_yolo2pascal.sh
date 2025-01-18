#!/bin/bash

# パラメータ設定
YOLO_DIR="annotations"      # YOLOアノテーションファイルのディレクトリ
IMAGE_DIR="images"               # 対応する画像ファイルのディレクトリ
VOC_DIR="dattaset"        # 出力先のPascal VOC形式アノテーションディレクトリ
CLASS_FILE="class_file"         # クラス名を定義したテキストファイル

# 出力ディレクトリ作成
mkdir -p $VOC_DIR

# 実行コマンド
python3 yolo2pascal.py \
    --yolo_dir $YOLO_DIR \
    --image_dir $IMAGE_DIR \
    --voc_dir $VOC_DIR \
    --class_file $CLASS_FILE

# 実行結果表示
if [ $? -eq 0 ]; then
    echo "変換成功: 出力ディレクトリ -> $VOC_DIR"
else
    echo "変換失敗: エラーログを確認してください。"
fi
