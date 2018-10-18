import copy
import numpy as np
import tensorflow as tf
import os
import random
import game
from ANN import *
from ReplayBuffer import *

DATA_DIRS = ["data/2016/freestyle1/", "data/2016/freestyle2/", "data/2016/freestyle3/", \
             "data/2017/freestyle1/", "data/2017/freestyle2/", "data/2017/freestyle3/"]
LOG_DIR = "logs/"
TEST_EVERY_EPOCH = 1000
LOSS_SUMMARY_EPOCH = 10
DUMP_EPOCH = 100
NB_FIGHT_EVAL = 100
UPDATE_THRESHOLD = 0.5
SAVE_FILE = "save/model.ckpt"
REPLAY_SIZE = 1000
START_TRAINING = 1000
BATCH_SIZE = 32

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

def fight(ann, best, dump=False):
    board = game.getEmptyBoard()
    current = 'O'
    action = random.randint(0, game.BOARD_SIZE * game.BOARD_SIZE - 1)
    board, won = game.move(board, action, current)
    if dump:
        print(game.render(board))
    current = 'O' if current == 'X' else 'X'
    while True:
        entry = state_lists_to_batch([board], current)
        probs = best(entry)[0] if current == 'O' else ann(entry)[0]
        while True:
            action = np.argmax(probs)
            if action not in game.possible_moves(board):
                probs[action] = -np.inf
            else:
                break
        board, won = game.move(board, action, current)
        if dump:
            print(game.render(board))
        if len(game.possible_moves(board)) == 0:
            return None
        if won:
            break
        current = 'O' if current == 'X' else 'X'
    return best if current == 'O' else ann

def eval(ann, best):
    ann_win = 0.0
    best_win = 0.0
    for i in range(NB_FIGHT_EVAL):
        winner = fight(ann, best, dump = (i == 0))
        if winner == ann:
            ann_win += 1.0
        elif winner == best:
            best_win += 1.0
    return ann_win / (ann_win + best_win)

if __name__ == "__main__":

    ann = ANN("Main_ANN")
    best = ANN("Best_ANN")
    replay = ReplayBuffer(REPLAY_SIZE)

    while len(replay) < START_TRAINING:
        file = getRandomFile()
        try:
            entries, outs = load(file)
            replay.extend(list(zip(entries, outs)))
        except ValueError:
            print("Invalid file:", file)
            continue

    summary_writer = tf.summary.FileWriter(LOG_DIR)
    loss_placeholder = tf.placeholder(tf.float32, ())
    loss_summary = tf.summary.scalar("Loss", loss_placeholder)
    eval_placeholder = tf.placeholder(tf.float32, ())
    eval_summary = tf.summary.scalar("Evaluation", eval_placeholder)

    saver = tf.train.Saver()

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        epoch = 0
        eval_idx = 0
        while True:
            epoch += 1

            file = getRandomFile()
            try:
                entries, outs = load(file)
                replay.extend(list(zip(entries, outs)))
            except ValueError:
                print("Invalid file:", file)
                continue

            sample = replay(BATCH_SIZE)
            entries, outs = zip(*sample)

            loss = ann.train(entries, outs)

            if epoch % TEST_EVERY_EPOCH == 0:
                eval_idx += 1
                result = eval(ann, best)
                sum = sess.run(eval_summary, feed_dict={eval_placeholder: result})
                summary_writer.add_summary(sum, eval_idx)
                print("EVALUATION: %f win against the last best ann" % (result))
                if result > UPDATE_THRESHOLD:
                    best.assign(ann)
                    print("The current ann become the best one")
                    saver.save(sess, SAVE_FILE)

            if epoch % LOSS_SUMMARY_EPOCH == 0:
                sum = sess.run(loss_summary, feed_dict={loss_placeholder: loss})
                summary_writer.add_summary(sum, epoch)

            if epoch % DUMP_EPOCH == 0:
                print("%d: Loss: %f" % (epoch, loss))
