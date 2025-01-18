import os
import pandas as pd
from PIL import Image
import argparse
from tqdm import tqdm
import logging

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

def process_images(csv_path, base_image_path, images_base_path, output_dir, log_file):
    """
    単一のBase画像を使用して、指定された領域を他の画像に上書きするスクリプト。

    Args:
        csv_path (str): CSVファイルのパス
        base_image_path (str): Base画像のパス
        images_base_path (str): 上書き対象画像のベースディレクトリ
        output_dir (str): 処理後の画像を保存するディレクトリ
        log_file (str): ログファイルのパス
    """
    setup_logger(log_file)

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # Base画像をロード
    try:
        base_image = Image.open(base_image_path)
    except Exception as e:
        logging.error(f"Error loading base image: {e}")
        return

    # CSVデータを読み込む
    try:
        data = pd.read_csv(csv_path)
    except Exception as e:
        logging.error(f"Error loading CSV file: {e}")
        return

    total = len(data)
    logging.info(f"Starting processing {total} entries from {csv_path}")

    # CSVデータの各行を処理
    for _, row in tqdm(data.iterrows(), total=total, desc="Processing images"):
        directory = row['Directory']
        image_file = row['ImageFile']

        # 元画像のパスを組み立て
        image_path = os.path.join(images_base_path, f"{directory}_{image_file}")
        
        # 画像が存在しない場合はスキップ
        if not os.path.exists(image_path):
            logging.warning(f"Image not found: {image_path}")
            continue

        try:
            # 上書き対象の画像を読み込む
            modified_image = Image.open(image_path)

            # 指定領域をBase画像から取得し、上書き
            box_x1, box_y1, box_x2, box_y2 = int(row['box_x1']), int(row['box_y1']), int(row['box_x2']), int(row['box_y2'])
            region = (box_x1, box_y1, box_x2, box_y2)
            patch = base_image.crop(region)
            modified_image.paste(patch, region)

            # 処理後の画像を保存
            output_image_path = os.path.join(output_dir, f"{directory}_{image_file}")
            modified_image.save(output_image_path)
            logging.info(f"Processed and saved: {output_image_path}")

        except Exception as e:
            logging.error(f"Error processing {image_path}: {e}")

    logging.info("Processing complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process images using a base image.")
    parser.add_argument('--csv_path', required=True, help="Path to the CSV file.")
    parser.add_argument('--base_image_path', required=True, help="Path to the base image.")
    parser.add_argument('--images_base_path', required=True, help="Base directory containing target images.")
    parser.add_argument('--output_dir', required=True, help="Directory to save processed images.")
    parser.add_argument('--log_file', default="process_images.log", help="Path to the log file.")

    args = parser.parse_args()

    process_images(
        csv_path=args.csv_path,
        base_image_path=args.base_image_path,
        images_base_path=args.images_base_path,
        output_dir=args.output_dir,
        log_file=args.log_file
    )
