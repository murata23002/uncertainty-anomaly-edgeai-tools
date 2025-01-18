import glob
import hashlib
import io
import os
import random
import sys
import xml.etree.ElementTree as ET

import pandas as pd
import tensorflow as tf
from object_detection.utils import dataset_util
from PIL import Image

""" INSTRUCTION
This script performs the following:
(1) Divides dataset into training and evaluation (90:10)
(2) Shuffles the dataset before converting it into TFrecords


Expected directories structure:
VOC_dataset 
   -JPEGImages
   -Annotations
    convert_to_tfrecord.py (this script)

To run this script:
$ python convert_to_tfrecord.py 

END INSTRUCTION """


def create_example(xml_file):
    # process the xml file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    image_name = root.find("filename").text
    file_name = image_name.encode("utf8")
    size = root.find("size")
    width = int(size[0].text)
    height = int(size[1].text)
    xmin = []
    ymin = []
    xmax = []
    ymax = []
    classes = []
    classes_text = []
    truncated = []
    poses = []
    difficult_obj = []
    for member in root.findall("object"):
        classes_text.append("Doraemon".encode("utf8"))
        xmin.append(float(member[4][0].text) / width)
        ymin.append(float(member[4][1].text) / height)
        xmax.append(float(member[4][2].text) / width)
        ymax.append(float(member[4][3].text) / height)
        difficult_obj.append(0)
        # For multiple classes, change the code block to read
        # the classes from the Annotations xml as following:
        """
           def class_text_to_int(row_label):
              if row_label == 'Doraemon':
                  return 1
              if row_label == 'Tanuki':
                  return 2
          and so on.....
           """
        classes.append(1)  # This example uses only one class (Doraemon)
        truncated.append(0)
        poses.append("Unspecified".encode("utf8"))

    # Read corresponding images (JPEGImages folder)
    full_path = os.path.join(
        "./JPEGImages", "{}".format(image_name)
    )  # provide the path of images directory
    with tf.gfile.GFile(full_path, "rb") as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    if image.format != "JPEG":
        raise ValueError("Image format not JPEG")
    key = hashlib.sha256(encoded_jpg).hexdigest()

    # Create TFRecord
    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "image/height": dataset_util.int64_feature(height),
                "image/width": dataset_util.int64_feature(width),
                "image/filename": dataset_util.bytes_feature(file_name),
                "image/source_id": dataset_util.bytes_feature(file_name),
                "image/key/sha256": dataset_util.bytes_feature(key.encode("utf8")),
                "image/encoded": dataset_util.bytes_feature(encoded_jpg),
                "image/format": dataset_util.bytes_feature("jpeg".encode("utf8")),
                "image/object/bbox/xmin": dataset_util.float_list_feature(xmin),
                "image/object/bbox/xmax": dataset_util.float_list_feature(xmax),
                "image/object/bbox/ymin": dataset_util.float_list_feature(ymin),
                "image/object/bbox/ymax": dataset_util.float_list_feature(ymax),
                "image/object/class/text": dataset_util.bytes_list_feature(
                    classes_text
                ),
                "image/object/class/label": dataset_util.int64_list_feature(classes),
                "image/object/difficult": dataset_util.int64_list_feature(
                    difficult_obj
                ),
                "image/object/truncated": dataset_util.int64_list_feature(truncated),
                "image/object/view": dataset_util.bytes_list_feature(poses),
            }
        )
    )
    return example


def main(path):
    writer_train = tf.python_io.TFRecordWriter("train.record")
    writer_test = tf.python_io.TFRecordWriter("test.record")
    filename_list = tf.train.match_filenames_once(f"{path}*.xml")
    init = (tf.global_variables_initializer(), tf.local_variables_initializer())
    sess = tf.Session()
    sess.run(init)
    list = sess.run(filename_list)
    random.shuffle(list)  # shuffle files list
    i = 1
    tst = 0  # to count number of images for evaluation
    trn = 0  # to count number of images for training
    for xml_file in list:
        example = create_example(xml_file)
        if (i % 10) == 0:  # each 10th file (xml and image) write it for evaluation
            writer_test.write(example.SerializeToString())
            tst = tst + 1
        else:  # the rest for training
            writer_train.write(example.SerializeToString())
            trn = trn + 1
        i = i + 1
        print(xml_file)
    writer_test.close()
    writer_train.close()
    print("Successfully converted dataset to TFRecord.")
    print("training dataset: # ")
    print(trn)
    print("test dataset: # ")
    print(tst)


if __name__ == "__main__":
    args = sys.argv
    path = args[1]
    main(path)
