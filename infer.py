
import numpy as np
from PIL import Image

import caffe
import sys

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
im = Image.open('data/mass_merged/test/sat/22828930_15.tiff')
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ -= np.array((95.58390035,97.0751154,89.11036257))
in_ = in_.transpose((2,0,1))

# init
caffe.set_device(int(sys.argv[1]))
caffe.set_mode_gpu()

# load net
net = caffe.Net('fcn8/deploy.prototxt', 'fcn8/snapshot/train_iter_1000.caffemodel', caffe.TEST)
# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
print '------------------------------------------------------------------------------------------'
# run net and take argmax for prediction
net.forward()
print '------------------------------------------------------------------------------------------'
out = net.blobs['score'].data[0]
print out[0:3,0:3,:]