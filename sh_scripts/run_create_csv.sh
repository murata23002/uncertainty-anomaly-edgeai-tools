#!/bin/bash

# 実行設定
BASE_DIR="dist"                          # ベースディレクトリ
SELECTED_DIR="scripts/selected"          # CSVファイルがあるディレクトリ
LOG_FILE="processing_log.txt"                                   # ログファイル
RANDOM_DIR_COUNT=500                                            # ランダムに選ぶディレクトリ数

# ステップ1: CSVファイルをループで処理
for CSV_FILE in "$SELECTED_DIR"/*.csv; do
    # CSVファイル名からディレクトリ名を生成 (拡張子.csvを除く)
    FILE_NAME=$(basename "$CSV_FILE" .csv)  # 拡張子なしのファイル名を取得
    OUTPUT_DIR="${FILE_NAME}"  # 出力ディレクトリ名
    
    # 出力ディレクトリが存在しない場合は作成
    mkdir -p "$OUTPUT_DIR"

    # 処理開始メッセージ
    echo "Processing: $CSV_FILE => Output Directory: $OUTPUT_DIR"

    # ステップ2: 画像を処理して保存
    python3 selpng2jpg.py --base_dir "$BASE_DIR" --csv_path "$CSV_FILE" --output_dir "$OUTPUT_DIR" --log_file "$LOG_FILE"

    # 終了メッセージ (ファイルごとにログ出力)
    echo "Finished processing $CSV_FILE. Logs are saved in $LOG_FILE"
done

# 全体の処理完了メッセージ
echo "All processing completed. Logs are saved in $LOG_FILE"
