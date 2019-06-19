#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : create_int8_trt.py
#   Author      : YunYang1994
#   Created date: 2019-06-15 13:26:02
#   Description :
#
#================================================================

import uff
import glob
from random import shuffle
import numpy as np
from tensorrt.parsers import uffparser
import tensorrt as trt

import calibrator

MEAN = (71.60167789, 82.09696889, 72.30508881)
CITYSCAPES_DIR = './data/images/'
CALIBRATION_DATASET_LOC = CITYSCAPES_DIR + '*.jpg'

CLASSES = 10
CHANNEL = 1
HEIGHT = 28
WIDTH = 28


def sub_mean_chw(data):
    _R_MEAN = 123.68 # ADJUST
    _G_MEAN = 116.78 # ADJUST
    _B_MEAN = 103.94 # ADJUST
    _CHANNEL_MEANS = [_R_MEAN, _G_MEAN, _B_MEAN]
    means = np.expand_dims(np.expand_dims(_CHANNEL_MEANS, 0), 0)
    data = data - means
    data = data.transpose([2,0,1]).astype(np.float32)
    data = data.copy(order='C')
    return data


def create_calibration_dataset():
    calibration_files = glob.glob(CALIBRATION_DATASET_LOC)
    shuffle(calibration_files)
    return calibration_files


print("Loading image files...")
calibration_files = create_calibration_dataset()
batchstream = calibrator.ImageBatchStream(5, calibration_files, sub_mean_chw)
print("Map image data from float to int8...")
int8_calibrator = calibrator.PythonEntropyCalibrator(["input_tensor"], batchstream)

G_LOGGER = trt.infer.ConsoleLogger(trt.infer.LogSeverity.INFO)
parser = uffparser.create_uff_parser()
parser.register_input("input_tensor", (3,224,224), 0)
parser.register_output("softmax_tensor")

pb_file = "./resnetv2_imagenet.pb"
uff_model = uff.from_tensorflow_frozen_model(pb_file, ["softmax_tensor"])

engine = trt.utils.uff_to_trt_engine(G_LOGGER, uff_model, parser, 1, 1 << 30, trt.infer.DataType.INT8, calibrator=int8_calibrator)
trt.utils.write_engine_to_file("./resnet.engine", engine.serialize())


