import json
import os


def get_label_for_imagenet_class(class_idx):
    labels_path = os.path.join(
        os.path.dirname(__file__), 'imagenet_labels.json')
    labels_map = json.load(open(labels_path, 'r'))
    return labels_map[str(class_idx)]
