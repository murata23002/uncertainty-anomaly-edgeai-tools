import os
import random
import argparse
import pandas as pd

def select_random_images(input_dir, output_csv, num_images):
    """
    指定されたディレクトリからランダムに画像ファイルを選択し、CSVに保存。

    Args:
        input_dir (str): 画像ファイルが保存されているディレクトリ。
        output_csv (str): 選択された画像ファイル名を保存するCSVファイル。
        num_images (int): 選択する画像ファイルの数。
    """
    # 指定ディレクトリから画像ファイルをリスト化
    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # 選択する画像数が全体より多い場合は全てを選択
    if num_images > len(image_files):
        print(f"Warning: Requested {num_images} images, but only {len(image_files)} available.")
        num_images = len(image_files)

    # ランダムに画像を選択
    selected_files = random.sample(image_files, num_images)

    # 選択されたファイルをCSVに保存
    selected_df = pd.DataFrame({'FileName': selected_files})
    selected_df.to_csv(output_csv, index=False)

    print(f"Randomly selected {num_images} images saved to {output_csv}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Select random images from a directory and save to CSV.")
    parser.add_argument('--input_dir', required=True, help="Directory containing image files.")
    parser.add_argument('--output_csv', required=True, help="Output CSV file to save selected images.")
    parser.add_argument('--num_images', type=int, default=10, help="Number of images to select randomly (default: 10).")

    args = parser.parse_args()

    select_random_images(
        input_dir=args.input_dir,
        output_csv=args.output_csv,
        num_images=args.num_images
    )
