#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : trt_inference.py
#   Author      : YunYang1994
#   Created date: 2019-05-10 11:38:29
#   Description :
#
#================================================================

import json
import time
import pycuda.autoinit
import numpy as np
import tensorrt as trt
from PIL import Image
import pycuda.driver as cuda # For automatic creation and cleanup of CUDA context


_R_MEAN = 123.68 # ADJUST
_G_MEAN = 116.78 # ADJUST
_B_MEAN = 103.94 # ADJUST
_CHANNEL_MEANS = [_R_MEAN, _G_MEAN, _B_MEAN]
CLASSES = json.loads(open("./data/label.json").read())
means = np.expand_dims(np.expand_dims(_CHANNEL_MEANS, 0), 0)

G_LOGGER = trt.infer.ConsoleLogger(trt.infer.LogSeverity.ERROR)
engine = trt.utils.load_engine(G_LOGGER, "./resnet.engine")
context = engine.create_execution_context()
stream = cuda.Stream()


image_data = np.array(Image.open("./data/images/elephant.jpg")) - means
# Covert image to CHW Numpy array (TensorRT expects CHW data)
image_data = image_data.transpose([2,0,1]).astype(np.float32)
image_data = image_data.copy(order='C')


def infer(context, input_img, batch_size):
    #load engine
    engine = context.get_engine()
    assert(engine.get_nb_bindings() == 2)
    #create output array to receive data
    dims = engine.get_binding_dimensions(1).to_DimsCHW()
    elt_count = dims.C() * dims.H() * dims.W() * batch_size
    #convert input data to Float32
    input_img = input_img.astype(np.float32)
    #Allocate pagelocked memory
    output = cuda.pagelocked_empty(elt_count, dtype=np.float32)

    #alocate device memory
    d_input = cuda.mem_alloc(batch_size * input_img.size * input_img.dtype.itemsize)
    d_output = cuda.mem_alloc(batch_size * output.size * output.dtype.itemsize)

    bindings = [int(d_input), int(d_output)]

    stream = cuda.Stream()

    #transfer input data to device
    cuda.memcpy_htod_async(d_input, input_img, stream)
    #execute model
    context.enqueue(batch_size, bindings, stream.handle, None)
    #transfer predictions back
    cuda.memcpy_dtoh_async(output, d_output, stream)

    #return predictions
    return output

infer_time = []
for i in range(50):
    s_time = time.time()
    result = infer(context, image_data, 1)
    stream.synchronize()
    e_time = time.time()
    infer_time.append(e_time - s_time)
    print(1000*(e_time - s_time), " ms")

print("=>", CLASSES[str(np.argmax(result))])



