import tensorflow as tf
import game

LEARNING_RATE = 0.01

class ANN:
    def __init__(self, scope=""):
        self.scope = scope

        with tf.variable_scope(self.scope):
            self._create_ann()

    def _create_ann(self):
        self.x = tf.placeholder(tf.float32, (None, game.BOARD_SIZE, game.BOARD_SIZE, 2))
        layer1 = tf.layers.conv2d(self.x, 4, 5, padding="same", activation=tf.nn.selu, \
                                  name="layer1")
        layer2 = tf.layers.conv2d(layer1, 4, 5, padding="same", activation=tf.nn.selu, \
                                  name="layer2")
        layer3 = tf.layers.conv2d(layer2, 8, 3, padding="same", activation=tf.nn.selu, \
                                  name="layer3")
        layer4 = tf.layers.conv2d(layer3, 8, 3, padding="same", activation=tf.nn.selu, \
                                  name="layer4")
        out = tf.layers.conv2d(layer4, 1, 1, padding="same", activation=tf.nn.selu, \
                                  name="out")
        self.out_flat = tf.contrib.layers.flatten(out)

        self.expected_y = tf.placeholder(tf.int32, (None))
        self.loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=self.expected_y, logits=self.out_flat))
        optimizer = tf.train.AdamOptimizer(LEARNING_RATE)
        self.training_op = optimizer.minimize(self.loss)

    def __call__(self, entries):
        session = tf.get_default_session()

        return session.run(self.out_flat, feed_dict={self.x: entries})

    def assign(self, otherANN):
        session = tf.get_default_session()
        all_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self.scope)
        all_other_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=otherANN.scope)
        for i, var in enumerate(all_variables):
            session.run(tf.assign(var, all_other_variables[i]))

    def train(self, entries, expected_outs):
        session = tf.get_default_session()

        loss, _ = session.run([self.loss, self.training_op], \
                              feed_dict={self.x: entries, \
                                         self.expected_y: expected_outs})
        return loss
