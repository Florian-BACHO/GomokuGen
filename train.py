import copy
import numpy as np
import tensorflow as tf
import os
import random
import game

DATA_DIRS = ["data/2016/freestyle1/", "data/2016/freestyle2/", "data/2016/freestyle3/", \
             "data/2017/freestyle1/", "data/2017/freestyle2/", "data/2017/freestyle3/"]
LOG_DIR = "logs/"
LEARNING_RATE = 0.01
TEST_EVERY_EPOCH = 1000
DUMP_EPOCH = 100

def loadDataFiles(dirs):
    out = []
    for it in dirs:
        files = os.listdir(it)
        out.extend([it + i for i in files])
    return out

DATA_FILES = loadDataFiles(DATA_DIRS)

def list_to_batch(dest, board, who_move):
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == who_move:
                dest[y, x, 0] = 1.0
            elif col != ' ':
                dest[y, x, 1] = 1.0

def state_lists_to_batch(state_lists, who_moves):
    out = np.zeros((len(state_lists), game.BOARD_SIZE, game.BOARD_SIZE, 2), dtype=np.float32)
    for idx, state in enumerate(state_lists):
        list_to_batch(out[idx], state, who_moves)
    return out

def load(file):
    f = open(file, "r")
    _ = f.readline()

    entries = []
    outs = []
    board = game.getEmptyBoard()
    current = 'O'
    for line in f.readlines():
        if not line[0].isdigit():
            break
        nums = [int(n) for n in line.split(',')]
        entries.append(copy.deepcopy(board))
        board[nums[0] - 1][nums[1] - 1] = current
        outs.append((nums[0] - 1) * game.BOARD_SIZE + nums[1] - 1)
        current = 'O' if current == 'X' else 'X'

    winner = 'O' if current == 'X' else 'X'

    i = 'O'
    entries_final = []
    outs_final = []
    for entry, out in zip(entries, outs):
        if i == winner:
            entries_final.append(entry)
            outs_final.append(out)
        i = 'O' if i == 'X' else 'X'
    return state_lists_to_batch(entries_final, winner), outs_final

def getRandomFile():
    return random.choice(DATA_FILES)

def test(session, x, y):
    board = game.getEmptyBoard()
    current = 'O'
    action = random.randint(0, game.BOARD_SIZE * game.BOARD_SIZE - 1)
    board, won = game.move(board, action, current)
    print(game.render(board))
    current = 'O' if current == 'X' else 'X'
    while True:
        probs = session.run(y, feed_dict={x: state_lists_to_batch([board], current)})[0]
        while True:
            action = np.argmax(probs)
            if action not in game.possible_moves(board):
                probs[action] = -np.inf
            else:
                break
        board, won = game.move(board, action, current)
        print(game.render(board))
        if won:
            break
        current = 'O' if current == 'X' else 'X'

if __name__ == "__main__":
    x = tf.placeholder(tf.float32, (None, game.BOARD_SIZE, game.BOARD_SIZE, 2))
    layer1 = tf.layers.conv2d(x, 4, 5, padding="same", activation=tf.nn.selu)
    layer2 = tf.layers.conv2d(layer1, 4, 5, padding="same", activation=tf.nn.selu)
    layer3 = tf.layers.conv2d(layer2, 8, 3, padding="same", activation=tf.nn.selu)
    layer4 = tf.layers.conv2d(layer3, 8, 3, padding="same", activation=tf.nn.selu)
    out = tf.layers.conv2d(layer4, 1, 1, padding="same", activation=tf.nn.selu)
    out_flat = tf.contrib.layers.flatten(out)

    expected_y = tf.placeholder(tf.int32, (None))
    loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=expected_y, logits=out_flat)
    optimizer = tf.train.AdamOptimizer(LEARNING_RATE)
    training_op = optimizer.minimize(loss)

    summary_writer = tf.summary.FileWriter(LOG_DIR)
    loss_summary = tf.summary.scalar("Loss", tf.reduce_mean(loss))

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        epoch = 0
        while True:
            epoch += 1
            file = getRandomFile()
            try:
                entries, outs = load(file)
            except ValueError:
                print("Invalid file:", file)
                continue
            loss_v, sum, _ = sess.run([loss, loss_summary, training_op], \
                                 feed_dict={x: entries, expected_y: outs})
            summary_writer.add_summary(sum, epoch)
            if epoch % TEST_EVERY_EPOCH == 0:
                test(sess, x, out_flat)
            if epoch % DUMP_EPOCH == 0:
                print("%d: Loss: %f" % (epoch, loss_v.mean()))
