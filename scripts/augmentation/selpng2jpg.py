import os
import shutil
import pandas as pd
import argparse
from tqdm import tqdm
import logging
from PIL import Image


def setup_logger(log_file):
    """
    ロガーを設定する。
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def convert_to_jpg(src_path, dest_path):
    """
    PNGをJPGに変換して保存する。
    
    Args:
        src_path (str): 元画像のパス
        dest_path (str): 変換後の保存先パス (.jpg)
    """
    try:
        with Image.open(src_path) as img:
            # RGBモードに変換（JPGでは必須）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(dest_path, "JPEG")
        return True
    except Exception as e:
        logging.error(f"Error converting {src_path} to JPG: {e}")
        return False


def copy_images(csv_path, base_dir, output_dir, log_file):
    """
    CSVを元に画像ファイルをコピーし、PNGをJPGに変換する。

    Args:
        csv_path (str): CSVファイルのパス
        base_dir (str): 元画像ファイルのベースディレクトリ
        output_dir (str): コピー先のディレクトリ
        log_file (str): ログファイルのパス
    """
    setup_logger(log_file)

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # CSVを読み込む
    try:
        data = pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        return

    total = len(data)
    logging.info(f"Starting to copy and convert {total} files from {csv_path}")

    # 処理件数のカウント
    success_count = 0
    error_count = 0

    # 各行を処理
    for _, row in tqdm(data.iterrows(), total=total, desc="Copying and converting files"):
        directory = row['Directory']
        image_file = row['ImageFile']

        # 拡張子を取得
        filename_base = os.path.splitext(image_file)[0]  # 拡張子除去

        # 元ファイルのパスを構築（拡張子を2パターン試す）
        png_path = os.path.join(base_dir, directory, "images", f"{filename_base}.png")
        jpg_path = os.path.join(base_dir, directory, "images", f"{filename_base}.jpg")

        # 出力先パス
        dest_path = os.path.join(output_dir, f"{directory}_{filename_base}.jpg")  # 出力は常にJPG形式

        # ファイルを処理
        try:
            if os.path.exists(png_path):  # PNGファイルが存在する場合
                success = convert_to_jpg(png_path, dest_path)
                if success:
                    logging.info(f"Converted and saved: {png_path} -> {dest_path}")
                    success_count += 1
                else:
                    logging.error(f"Failed to convert: {png_path}")
                    error_count += 1
            elif os.path.exists(jpg_path):  # JPGファイルが存在する場合
                shutil.copy(jpg_path, dest_path)
                logging.info(f"Copied: {jpg_path} -> {dest_path}")
                success_count += 1
            else:
                logging.warning(f"Source file not found for both PNG and JPG: {png_path}, {jpg_path}")
                error_count += 1
        except Exception as e:
            logging.error(f"Error processing file {filename_base}: {e}")
            error_count += 1

    # 処理結果のログと出力
    logging.info(f"File copy and conversion process complete. Total: {total}, Success: {success_count}, Errors: {error_count}")
    print(f"Process completed. Total: {total}, Success: {success_count}, Errors: {error_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy and convert images based on a CSV file.")
    parser.add_argument('--csv_path', required=True, help="Path to the CSV file.")
    parser.add_argument('--base_dir', required=True, help="Base directory containing the source files.")
    parser.add_argument('--output_dir', required=True, help="Directory to copy files to.")
    parser.add_argument('--log_file', default="copy_images.log", help="Path to the log file.")

    args = parser.parse_args()

    copy_images(
        csv_path=args.csv_path,
        base_dir=args.base_dir,
        output_dir=args.output_dir,
        log_file=args.log_file
    )
