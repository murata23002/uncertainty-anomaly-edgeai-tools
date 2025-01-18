#!/bin/bash

# Set variables
TARGET_FILE_LIST="taget_file_list.csv"
FILE_LIST="file_list.csv"
BASE_DIR="dist"
OUTPUT_DIR="output"

# Run Python script
python3 draw_rectangles.py \
    --target_file_list "$TARGET_FILE_LIST" \
    --file_list "$FILE_LIST" \
    --base_dir "$BASE_DIR" \
    --output_dir "$OUTPUT_DIR"
