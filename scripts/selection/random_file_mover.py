import os
import random
import shutil
import sys
from sys import argv


def move_random_files(source_directory, destination_directory, num_files):
    train_images = os.path.join(source_directory, "images")
    train_annotations = os.path.join(source_directory, "annotations")

    destination_images = os.path.join(destination_directory, "images")
    destination_annotations = os.path.join(destination_directory, "annotations")
    # 指定されたディレクトリからファイル一覧を取得
    files = os.listdir(train_images)

    # ファイルが存在しない場合は終了
    if not files:
        print("指定されたディレクトリにファイルがありません。")
        return

    # 移動するファイルの数を指定
    num_files = min(num_files, len(files))

    # ランダムにファイルを選択
    random_files = random.sample(files, num_files)

    for random_file in random_files:

        source_path_image = os.path.join(train_images, random_file)
        source_xml_file_name = os.path.join(
            train_annotations, os.path.splitext(random_file)[0] + ".xml"
        )

        try:
            # アノテーションファイルを移動
            shutil.move(source_path_image, destination_images)
            print(
                f"アノテーションファイル {random_file} を {destination_directory}/annotations に移動しました。"
            )

            # 画像ファイルを移動
            shutil.move(source_xml_file_name, destination_annotations)
            print(
                f"画像ファイル {source_xml_file_name} を {destination_directory}/images に移動しました."
            )
        except Exception as e:
            print(f"ファイルの移動中にエラーが発生しました: {e}")


# 使用例
args = sys.argv
source_directory = args[1]
destination_directory = args[2]
num_files_to_move = int(args[3])  # 移動するファイルの数を指定
print(f"source_directory = {source_directory}")
print(f"destination_directory = {destination_directory}")
print(f"num_files_to_move = {num_files_to_move}")
move_random_files(source_directory, destination_directory, num_files_to_move)
