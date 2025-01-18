import os
import json
#import tensorflow as tf
import cv2
import xml.etree.ElementTree as ET
import argparse

class DatasetConverter:
    def coco_to_pascal(self, coco_json, output_dir):
        try:
            with open(coco_json) as f:
                coco_data = json.load(f)
        except Exception as e:
            print(f"Error loading COCO JSON file: {e}")
            return
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for image_info in coco_data['images']:
            image_id = image_info['id']
            image_filename = image_info['file_name']
            height = image_info['height']
            width = image_info['width']
            
            annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]
            
            annotation_xml = self.create_pascal_annotation(image_filename, width, height, annotations, coco_data['categories'])
            annotation_path = os.path.join(output_dir, os.path.splitext(image_filename)[0] + '.xml')
            
            try:
                with open(annotation_path, 'w') as xml_file:
                    xml_file.write(annotation_xml)
            except Exception as e:
                print(f"Error writing Pascal VOC XML file: {e}")

    def create_pascal_annotation(self, image_filename, width, height, annotations, categories):
        annotation = ET.Element("annotation")
        
        folder = ET.SubElement(annotation, "folder").text = "images"
        filename = ET.SubElement(annotation, "filename").text = image_filename
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = str(width)
        ET.SubElement(size, "height").text = str(height)
        ET.SubElement(size, "depth").text = "3"
        
        for ann in annotations:
            obj = ET.SubElement(annotation, "object")
            category = next(cat for cat in categories if cat['id'] == ann['category_id'])
            ET.SubElement(obj, "name").text = category['name']
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = "0"
            ET.SubElement(obj, "difficult").text = "0"
            
            bbox = ET.SubElement(obj, "bndbox")
            x_min, y_min, width, height = ann['bbox']
            x_max = x_min + width
            y_max = y_min + height
            ET.SubElement(bbox, "xmin").text = str(int(x_min))
            ET.SubElement(bbox, "ymin").text = str(int(y_min))
            ET.SubElement(bbox, "xmax").text = str(int(x_max))
            ET.SubElement(bbox, "ymax").text = str(int(y_max))
        
        return ET.tostring(annotation, encoding='unicode')

    def pascal_to_coco(self, pascal_voc_dir, output_json):
        categories = []
        annotations = []
        images = []
        annotation_id = 1
        category_id_map = {}
        
        for xml_file in os.listdir(pascal_voc_dir):
            if not xml_file.endswith('.xml'):
                continue
            
            xml_path = os.path.join(pascal_voc_dir, xml_file)
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
            except Exception as e:
                print(f"Error parsing XML file {xml_path}: {e}")
                continue
            
            image_id = len(images) + 1
            filename = root.find('filename').text
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            
            images.append({
                'id': image_id,
                'file_name': filename,
                'width': width,
                'height': height
            })
            
            for obj in root.findall('object'):
                category_name = obj.find('name').text
                if category_name not in category_id_map:
                    category_id = len(categories) + 1
                    categories.append({
                        'id': category_id,
                        'name': category_name
                    })
                    category_id_map[category_name] = category_id
                else:
                    category_id = category_id_map[category_name]
                
                bbox = obj.find('bndbox')
                x_min = int(bbox.find('xmin').text)
                y_min = int(bbox.find('ymin').text)
                x_max = int(bbox.find('xmax').text)
                y_max = int(bbox.find('ymax').text)
                width = x_max - x_min
                height = y_max - y_min
                
                annotations.append({
                    'id': annotation_id,
                    'image_id': image_id,
                    'category_id': category_id,
                    'bbox': [x_min, y_min, width, height],
                    'area': width * height,
                    'iscrowd': 0
                })
                annotation_id += 1
        
        coco_format = {
            'images': images,
            'annotations': annotations,
            'categories': categories
        }
        
        try:
            with open(output_json, 'w') as f:
                json.dump(coco_format, f, indent=4)
        except Exception as e:
            print(f"Error writing COCO JSON file: {e}")
    
    def pascal_to_tfrecord(self, pascal_voc_dir, output_tfrecord):
        writer = tf.io.TFRecordWriter(output_tfrecord)
        
        for xml_file in os.listdir(pascal_voc_dir):
            if not xml_file.endswith('.xml'):
                continue
            
            xml_path = os.path.join(pascal_voc_dir, xml_file)
            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()
            except Exception as e:
                print(f"Error parsing XML file {xml_path}: {e}")
                continue
            
            filename = root.find('filename').text
            image_path = os.path.join(pascal_voc_dir, 'JPEGImages', filename)
            try:
                image = cv2.imread(image_path)
                height, width, _ = image.shape
            except Exception as e:
                print(f"Error reading image file {image_path}: {e}")
                continue
            
            try:
                with tf.io.gfile.GFile(image_path, 'rb') as fid:
                    encoded_image_data = fid.read()
            except Exception as e:
                print(f"Error reading image file {image_path}: {e}")
                continue
            
            tf_example = self.create_tf_example(root, encoded_image_data, height, width)
            writer.write(tf_example.SerializeToString())
        
        writer.close()

    def create_tf_example(self, root, encoded_image_data, height, width):
        filename = root.find('filename').text.encode('utf8')
        image_format = b'jpg'
        
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []
        
        for obj in root.findall('object'):
            x_min = int(obj.find('bndbox/xmin').text) / width
            x_max = int(obj.find('bndbox/xmax').text) / width
            y_min = int(obj.find('bndbox/ymin').text) / height
            y_max = int(obj.find('bndbox/ymax').text) / height
            
            xmins.append(x_min)
            xmaxs.append(x_max)
            ymins.append(y_min)
            ymaxs.append(y_max)
            
            class_text = obj.find('name').text.encode('utf8')
            classes_text.append(class_text)
            classes.append(1)  # Assuming all objects are of class 1. Modify as needed.
        
        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': self.int64_feature(height),
            'image/width': self.int64_feature(width),
            'image/filename': self.bytes_feature(filename),
            'image/source_id': self.bytes_feature(filename),
            'image/encoded': self.bytes_feature(encoded_image_data),
            'image/format': self.bytes_feature(image_format),
            'image/object/bbox/xmin': self.float_list_feature(xmins),
            'image/object/bbox/xmax': self.float_list_feature(xmaxs),
            'image/object/bbox/ymin': self.float_list_feature(ymins),
            'image/object/bbox/ymax': self.float_list_feature(ymaxs),
            'image/object/class/text': self.bytes_list_feature(classes_text),
            'image/object/class/label': self.int64_list_feature(classes),
        }))
        return tf_example

    def int64_feature(self, value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    def bytes_feature(self, value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def float_list_feature(self, value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))

    def int64_list_feature(self, value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

    def bytes_list_feature(self, value):
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))

def main(args):
    converter = DatasetConverter()
    if args.command == 'coco_to_pascal':
        converter.coco_to_pascal(args.input, args.output)
    elif args.command == 'pascal_to_coco':
        converter.pascal_to_coco(args.input, args.output)
    elif args.command == 'pascal_to_tfrecord':
        converter.pascal_to_tfrecord(args.input, args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset format converter")
    subparsers = parser.add_subparsers(dest="command")

    parser_coco_to_pascal = subparsers.add_parser('coco_to_pascal')
    parser_coco_to_pascal.add_argument('input', type=str, help="Path to COCO JSON file")
    parser_coco_to_pascal.add_argument('output', type=str, help="Output directory for PASCAL VOC XML files")

    parser_pascal_to_coco = subparsers.add_parser('pascal_to_coco')
    parser_pascal_to_coco.add_argument('input', type=str, help="Directory containing PASCAL VOC XML files")
    parser_pascal_to_coco.add_argument('output', type=str, help="Output COCO JSON file")

    parser_pascal_to_tfrecord = subparsers.add_parser('pascal_to_tfrecord')
    parser_pascal_to_tfrecord.add_argument('input', type=str, help="Directory containing PASCAL VOC XML files")
    parser_pascal_to_tfrecord.add_argument('output', type=str, help="Output TFRecord file")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
    else:
        main(args)

