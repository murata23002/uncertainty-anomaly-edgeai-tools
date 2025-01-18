import os
import random
import csv
import argparse

def create_csv(base_dir, csv_file, random_dir_count):
    # ベースディレクトリ内のサブディレクトリを探索
    directories = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ]

    # CSV作成
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Directory", "ImageFile"])  # ヘッダー行

        selected_dirs = []
        retries = 0

        # 指定数までランダムにディレクトリを選択
        while len(selected_dirs) < random_dir_count and directories:
            dir_path = random.choice(directories)
            directories.remove(dir_path)  # 一度選択したディレクトリは削除

            images_dir = os.path.join(dir_path, "images")
            if not os.path.exists(images_dir):  # imagesディレクトリが存在しない場合はスキップ
                retries += 1
                continue
            
            # images内の画像ファイルを取得
            images = [
                f for f in os.listdir(images_dir)
                if os.path.isfile(os.path.join(images_dir, f))
            ]

            if images:
                # ランダムに1つ選択
                selected_image = random.choice(images)
                writer.writerow([os.path.basename(dir_path), selected_image])
                selected_dirs.append(dir_path)
            else:
                retries += 1  # 空のディレクトリの場合も再選択

        if len(selected_dirs) < random_dir_count:
            print(f"Warning: Only {len(selected_dirs)} directories with valid images were found out of {random_dir_count} requested.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a CSV file of randomly selected images.")
    parser.add_argument("--base_dir", required=True, help="Base directory containing the data.")
    parser.add_argument("--csv_file", default="selected_images.csv", help="Output CSV file.")
    parser.add_argument("--random_dir_count", type=int, default=10, help="Number of directories to randomly select.")
    args = parser.parse_args()

    create_csv(args.base_dir, args.csv_file, args.random_dir_count)
