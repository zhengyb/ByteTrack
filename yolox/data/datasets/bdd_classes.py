#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

BDD_CLASSES = (
    "person",
    "car",
    "traffic sign",
    "traffic light",
    "bus",
    "truck",
    "rider",
    "motor",
    "bike",
    "train",
)

BDD_COLLISION_CLASSES = (
    "person",
    "car",
    "bus",
    "truck",
    "rider",
    "motor",
    "bike",
    "train",
)


def is_bdd_collision_class(cls_id):
    cls_name = BDD_CLASSES[cls_id]
    return cls_name in BDD_COLLISION_CLASSES
