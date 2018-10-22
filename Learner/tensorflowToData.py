import tensorflow as tf
import numpy as np
from ANN import *

SCOPE = "Best_ANN"
LAYERS = ["layer1", "layer2", "layer3", "layer4", "out"]

def getTensorWeights(tensor):
    name = tensor.name.split('/')[0]

def getKernelAndBias(sess, layerName):
    kernel = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, layerName + '/kernel')[0]
    bias = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, layerName + '/bias')[0]

    k, b = sess.run([kernel, bias])
    return k, b

def writeKernelAndBias(file, kernel, bias):
    for row in kernel:
        for col in row:
            for chan in col:
                for filter in chan:
                    file.write(str(filter) + "\n")

    for b in bias:
        file.write(str(b) + "\n")

ann = ANN(SCOPE)

saver = tf.train.Saver()

with tf.Session() as sess:
    saver.restore(sess, "save/model.ckpt")

    res = ann(np.zeros((1, 20, 20, 2)))
    print(res)

    file = open("out.model", "w")

    for name in LAYERS:
        kernel, bias = getKernelAndBias(sess, SCOPE + "/" + name)
        print(len(kernel))
        writeKernelAndBias(file, kernel, bias)

    file.close()
