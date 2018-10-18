import tensorflow as tf

def getTensorWeights(tensor):
    name = tensor.name.split('/')[0]

x = tf.placeholder(tf.float32, [None, 2, 2, 2])
conv1 = tf.layers.conv2d(x, 5, 3, padding="same", name="conv1")

kernel = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'conv1/kernel')[0]
bias = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'conv1/bias')[0]

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    res = sess.run(conv1, feed_dict={x: [[[[1, 0], [0, 0]],
                                          [[0, 0], [0, 0]]]]})

    print(res)

    k, b = sess.run([kernel, bias])
    print(k)
    file = open("out.model", "w")

    for row in k:
        for col in row:
            for chan in col:
                for filter in chan:
                    file.write(str(filter) + "\n")

    for bia in b:
        file.write(str(bia) + "\n")

    file.close()
