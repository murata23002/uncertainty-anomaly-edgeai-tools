import json
from collections import defaultdict

def count_annotations(coco_annotation_file):
    with open(coco_annotation_file, 'r') as f:
        coco_data = json.load(f)
    
    annotation_count = defaultdict(int)
    
    for annotation in coco_data['annotations']:
        category_id = annotation['category_id']
        annotation_count[category_id] += 1
    
    return annotation_count

# COCOアノテーションファイルのパスを指定
coco_annotation_file = ""

annotation_count = count_annotations(coco_annotation_file)

for category_id, count in annotation_count.items():
    print(f'Category ID {category_id}: {count} annotations')

