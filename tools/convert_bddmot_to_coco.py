#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Convert BDD100K MOT to COCO format
#
# Author: Reuben Zheng
# Date: 2025-03-14

import os
import numpy as np
import json
import argparse

from yolox.data.datasets.bdd_classes import BDD_CLASSES


BDDMOT_LABELS_PATH = "./datasets/bdd100k/labels"
COCOFMT_ANN_PATH = "./datasets/bdd100k/annotations"
IMAGE_BASE_PATH = "./datasets/bdd100k"

DATASET_SIZE = {
    "sample": {
        "train": 5,  # 5 videosthis_video_id
        "val": 2,  # 2 videos
    },
    "small": {"train": 140, "val": 20},
    "full": {"train": 0, "val": 0},
}


def get_args():
    parser = argparse.ArgumentParser(description="Convert BDD100K MOT to COCO format")
    parser.add_argument(
        "--size", type=str, default="sample", help="Dataset size, sample, small or full"
    )
    return parser.parse_args()


def uniform_cat_name(cat_name):
    if cat_name == "pedestrian":
        return "person"
    elif cat_name == "other person":
        return "person"
    elif cat_name == "bicycle":
        return "bike"
    elif cat_name == "motorcycle":
        return "motor"
    elif cat_name == "other vehicle":
        return "car"
    elif cat_name == "trailer":
        return "car"

    return cat_name


def bdd_cat_name_to_id_map(bdd_classes):
    bdd_cat_name_to_id = {}
    for i, cls in enumerate(bdd_classes):
        bdd_cat_name_to_id[cls] = i + 1
    return bdd_cat_name_to_id


BDD_CAT_NAME_TO_ID_MAP = bdd_cat_name_to_id_map(BDD_CLASSES)


def convert_cats_to_coco(bdd_classes):
    cats = []
    for i, cls in enumerate(bdd_classes):
        cats.append(
            {
                "id": i + 1,  # COCO uses 1-based index
                "name": cls,
            }
        )
    return cats


def convert_bddmot_labels_to_coco(
    bddmot_labels_path, coco_labels_path, cats, dataset_type="val", size="full"
):
    if not os.path.exists(coco_labels_path):
        os.makedirs(coco_labels_path, exist_ok=True)

    bddmot_ds_labels_path = os.path.join(bddmot_labels_path, dataset_type)
    coco_ds_label_filename = f"{coco_labels_path}/{dataset_type}.json"

    coco_ann = {"categories": cats, "videos": [], "images": [], "annotations": []}

    video_anns = []
    image_anns = []
    annotations = []
    bdd_track_ids = []
    for bddmot_video_label_filename in os.listdir(bddmot_ds_labels_path):
        with open(
            os.path.join(bddmot_ds_labels_path, bddmot_video_label_filename), "r"
        ) as f:
            # Extract video annotation
            video_name = bddmot_video_label_filename.split(".")[0]
            this_video_id = len(video_anns) + 1
            if this_video_id > DATASET_SIZE[size][dataset_type]:
                break

            print(f"Processing video {video_name} - {len(video_anns)}")
            this_video_ann = {
                "id": this_video_id,
                "file_name": video_name,
            }
            video_anns.append(this_video_ann)

            bddmot_video_labels = json.load(f)
            for bdd_image_label in bddmot_video_labels:
                # Extract image annotation
                frame_idx = bdd_image_label["frameIndex"] + 1
                this_image_id = len(image_anns) + 1
                this_img_name = video_name + "/" + bdd_image_label["name"]
                if not os.path.exists(
                    os.path.join(IMAGE_BASE_PATH, dataset_type, this_img_name)
                ):
                    print(f"Image {this_img_name} does not exist")
                    continue
                this_image_ann = {
                    "id": this_image_id,
                    "file_name": this_img_name,
                    "frame_id": frame_idx,
                    "prev_image_id": this_image_id - 1 if frame_idx > 1 else -1,
                    "next_image_id": this_image_id + 1,
                    "video_id": this_video_id,
                    "height": 1080,  # TODO
                    "width": 1920,  # TODO
                }
                image_anns.append(this_image_ann)

                for bdd_label in bdd_image_label["labels"]:
                    # Extract object annotation
                    # BDD MOT format:
                    #      {
                    #     "id": "00122376", # track id
                    #     "category": "car", # class name
                    #     "box2d": {
                    #       "x1": 874.5306926235825, # x1
                    #       "x2": 1042.2607513175765, # x2
                    #       "y1": 362.26229589226574, # y1
                    #       "y2": 459.4667292648439 # y2
                    #     }
                    #     }
                    # COCO format:
                    #         {
                    #    "id": 300, # anno id
                    #    "category_id": 1, # class id
                    #    "image_id": 302, # image id
                    #    "track_id": 1, # track id, globally unique
                    #    "bbox": [
                    #        1010.0, # x1
                    #        421.0, # y1
                    #        160.0,
                    #        461.0
                    #    ],
                    #    "conf": 1.0,
                    #    "iscrowd": 0,
                    #    "area": 73760.0
                    # },
                    bdd_track_id = bdd_label["id"]
                    if bdd_track_id not in bdd_track_ids:
                        bdd_track_ids.append(bdd_track_id)
                        this_track_id = len(bdd_track_ids)
                    else:
                        this_track_id = bdd_track_ids.index(bdd_track_id) + 1

                    this_anno = {
                        "id": len(annotations) + 1,
                        "category_id": BDD_CAT_NAME_TO_ID_MAP[
                            uniform_cat_name(bdd_label["category"])
                        ],
                        "image_id": this_image_id,
                        "track_id": this_track_id,
                        "bbox": [
                            bdd_label["box2d"]["x1"],
                            bdd_label["box2d"]["y1"],
                            bdd_label["box2d"]["x2"] - bdd_label["box2d"]["x1"],
                            bdd_label["box2d"]["y2"] - bdd_label["box2d"]["y1"],
                        ],
                        "area": (bdd_label["box2d"]["x2"] - bdd_label["box2d"]["x1"])
                        * (bdd_label["box2d"]["y2"] - bdd_label["box2d"]["y1"]),
                        "iscrowd": 0,
                        "conf": 1.0,
                    }
                    annotations.append(this_anno)

                    pass

            if len(image_anns) > 0:
                image_anns[-1]["next_image_id"] = -1

    coco_ann["videos"] = video_anns
    coco_ann["images"] = image_anns
    coco_ann["annotations"] = annotations
    with open(coco_ds_label_filename, "w") as f:
        json.dump(coco_ann, f)

    print(f"Video count: {len(video_anns)}")
    print(f"Image count: {len(image_anns)}")
    print(f"Annotation count: {len(annotations)}")
    print(f"COCO format labels saved to {coco_ds_label_filename}")


def main():
    args = get_args()

    coco_cats = convert_cats_to_coco(BDD_CLASSES)

    convert_bddmot_labels_to_coco(
        BDDMOT_LABELS_PATH,
        COCOFMT_ANN_PATH,
        coco_cats,
        dataset_type="val",
        size=args.size,
    )
    convert_bddmot_labels_to_coco(
        BDDMOT_LABELS_PATH,
        COCOFMT_ANN_PATH,
        coco_cats,
        dataset_type="train",
        size=args.size,
    )

    print(f"COCO format labels saved to {COCOFMT_ANN_PATH}")


if __name__ == "__main__":
    main()
