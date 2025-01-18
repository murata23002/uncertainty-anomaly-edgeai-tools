import os
import shutil
import pandas as pd
import argparse

def create_dataset(csv_file, image_dir, annotation_dir, output_image_dir, output_annotation_dir):
    # 出力ディレクトリの作成
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_annotation_dir, exist_ok=True)

    # CSVファイルの読み込み
    df = pd.read_csv(csv_file)

    # データセット作成処理
    for index, row in df.iterrows():
        data_time = str(row['data_time'])
        print(row)

        # 対象ファイル名を生成
        image_file = f'frame_{data_time}.jpg'
        annotation_file = f'frame_{data_time}.xml'

        # 画像ファイルのコピー
        src_image_path = os.path.join(image_dir, image_file)
        dst_image_path = os.path.join(output_image_dir, image_file)
        if os.path.exists(src_image_path):
            shutil.copy(src_image_path, dst_image_path)
            print(f'Copied image file: {image_file}')
        else:
            print(f'Image file not found: {image_file}')

        # アノテーションファイルのコピー
        src_annotation_path = os.path.join(annotation_dir, annotation_file)
        dst_annotation_path = os.path.join(output_annotation_dir, annotation_file)
        if os.path.exists(src_annotation_path):
            shutil.copy(src_annotation_path, dst_annotation_path)
            print(f'Copied annotation file: {annotation_file}')
        else:
            print(f'Annotation file not found: {annotation_file}')

    print('Dataset creation completed.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dataset by copying selected images and annotations.')
    parser.add_argument('--csv_file', required=True, help='Path to the CSV file containing dataset list')
    parser.add_argument('--image_dir', required=True, help='Path to the directory containing images')
    parser.add_argument('--annotation_dir', required=True, help='Path to the directory containing annotations')
    parser.add_argument('--output_image_dir', required=True, help='Output directory for selected images')
    parser.add_argument('--output_annotation_dir', required=True, help='Output directory for selected annotations')

    args = parser.parse_args()

    create_dataset(args.csv_file, args.image_dir, args.annotation_dir, args.output_image_dir, args.output_annotation_dir)
