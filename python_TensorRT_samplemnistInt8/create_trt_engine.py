#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : create_trt_engine.py
#   Author      : YunYang1994
#   Created date: 2019-03-21 10:29:32
#   Description :
#
#================================================================

import uff
import tensorrt as trt
from tensorrt.parsers import uffparser
G_LOGGER = trt.infer.ConsoleLogger(trt.infer.LogSeverity.INFO)

pb_file = "./resnetv2_imagenet.pb"
uff_model = uff.from_tensorflow_frozen_model(pb_file, ["softmax_tensor"])

parser = uffparser.create_uff_parser()
parser.register_input("input_tensor", (3,224,224), 0)
parser.register_output("softmax_tensor")

engine = trt.utils.uff_to_trt_engine(G_LOGGER, uff_model, parser, 1, 1 << 30, trt.infer.DataType.FLOAT)
trt.utils.write_engine_to_file("./resnet.engine", engine.serialize())

