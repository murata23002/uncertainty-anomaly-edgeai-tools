#!/bin/bash

# 引数を変数に設定
CSV_FILE="select_data_names_anomaly.csv"
IMAGE_DIR=""
ANNOTATION_DIR=""
OUTPUT_IMAGE_DIR="images"
OUTPUT_ANNOTATION_DIR="annotations"

# Pythonスクリプトの実行
python3 select_dataset.py \
    --csv_file "$CSV_FILE" \
    --image_dir "$IMAGE_DIR" \
    --annotation_dir "$ANNOTATION_DIR" \
    --output_image_dir "$OUTPUT_IMAGE_DIR" \
    --output_annotation_dir "$OUTPUT_ANNOTATION_DIR"
