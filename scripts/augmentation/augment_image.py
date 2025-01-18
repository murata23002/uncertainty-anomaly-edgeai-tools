import os
import random
import sys
import xml.etree.ElementTree as ET

from PIL import Image


def get_filename_without_extension(image_filename):
    split = image_filename.rsplit(".", 1)
    return (split[0], split[1])


def copy_and_save_xml(input_xml_file, output_xml_file, new_filename):
    # 元のXMLファイルを読み込む
    tree = ET.parse(input_xml_file)
    root = tree.getroot()

    # 新しいファイル名を設定
    for filename_elem in root.findall("filename"):
        filename_elem.text = new_filename + ".jpg"

    # XMLファイルを保存
    tree.write(output_xml_file)


def rgb2gray(input_directory, file_name):
    image_path = os.path.join(input_directory, file_name)
    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    new_file_name, extension = get_filename_without_extension(file_name)
    new_file_name = new_file_name + "_gray"
    return grayscale_image, new_file_name


def augment(source_directory, num_files, output_directory):
    images_directory = os.path.join(source_directory, "images")
    annotations_directory = os.path.join(source_directory, "annotations")

    out_images_directory = os.path.join(output_directory, "images")
    out_annotations_directory = os.path.join(output_directory, "annotations")
    image_files = os.listdir(images_directory)

    if not image_files:
        print("指定されたディレクトリに画像ファイルがありません。")
        return

    num_files = min(num_files, len(image_files))
    random_image_files = random.sample(image_files, num_files)

    for image_file in random_image_files:
        file_name, _ = get_filename_without_extension(image_file)
        gray_img, new_file_name = rgb2gray(images_directory, image_file)
        gray_img.save(os.path.join(out_images_directory, new_file_name + ".jpg"))
        copy_and_save_xml(
            os.path.join(annotations_directory, file_name + ".xml"),
            os.path.join(out_annotations_directory, new_file_name + ".xml"),
            new_file_name,
        )


if __name__ == "__main__":
    args = sys.argv
    source_directory = args[1]
    num_files_to_move = int(args[2])
    output_directory = args[3]

    augment(source_directory, num_files_to_move, output_directory)
