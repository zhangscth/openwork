#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : tf_inference.py
#   Author      : YunYang1994
#   Created date: 2019-05-10 11:41:54
#   Description :
#
#================================================================

import time
import numpy as np
import tensorflow as tf
from PIL import Image

_RESIZE_MIN = 256
_R_MEAN = 123.68 # ADJUST
_G_MEAN = 116.78 # ADJUST
_B_MEAN = 103.94 # ADJUST
_CHANNEL_MEANS = [_R_MEAN, _G_MEAN, _B_MEAN]
means = np.expand_dims(np.expand_dims(_CHANNEL_MEANS, 0), 0)

image_data = np.array(Image.open("./elephant.jpg")) - means
image_data = np.expand_dims(image_data, 0)

tf.reset_default_graph()
graph = tf.Graph()


with tf.gfile.FastGFile("./resnetv2_imagenet.pb", "rb") as f:
    frozen_graph_def = tf.GraphDef()
    frozen_graph_def.ParseFromString(f.read())


with graph.as_default():
    images = tf.placeholder("float", [1, 224, 224, 3])
    return_tensors = tf.import_graph_def(graph_def=frozen_graph_def,
                                        input_map={"input_tensor": images},
                                        return_elements=["softmax_tensor"])
    output = return_tensors[0].outputs[0]

with tf.Session(graph=graph) as sess:
    for i in range(50):
        s_time = time.time()
        result = sess.run([output], feed_dict={images: image_data})
        e_time = time.time()
        print(1000*(e_time - s_time), " ms")
        # print(np.argmax(result))



