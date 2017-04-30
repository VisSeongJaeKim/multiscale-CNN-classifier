import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.contrib.layers import flatten
import tensorflow as tf
from sklearn.utils import shuffle

def display_random_samples(x, y):
    names = pd.read_csv('signnames.csv')
    print(names['ClassId'][1])
    indices = np.random.rand(5) * x.shape[0]
    for i in indices:
        index = int(i)
        image = x[index, :, :, :]
        print(names['SignName'][y_train[index]])
        fig = plt.figure(frameon=False)
        fig.set_size_inches(1, 1)
        plt.imshow(image)
        plt.show()
        plt.close()


def display_random_samples_gray(x, y):
    names = pd.read_csv('signnames.csv')
    print(names['ClassId'][1])
    indices = np.random.rand(5) * x.shape[0]
    for i in indices:
        index = int(i)
        image = x[index, :, :]
        print(names['SignName'][y_train[index]])
        fig = plt.figure(frameon=False)
        fig.set_size_inches(1, 1)
        plt.imshow(image, cmap='gray')
        plt.show()
        plt.close()

def evaluate(X_data, y_data, accuracy_operation, BATCH_SIZE, x, y):
    num_examples = len(X_data)
    total_accuracy = 0
    sess = tf.get_default_session()
    for offset in range(0, num_examples, BATCH_SIZE):
        batch_x, batch_y = X_data[offset:offset + BATCH_SIZE], y_data[offset:offset + BATCH_SIZE]
        accuracy = sess.run(accuracy_operation, feed_dict={x: batch_x, y: batch_y})
        total_accuracy += (accuracy * len(batch_x))
    return total_accuracy / num_examples

def Architecture(x):
    # Arguments used for tf.truncated_normal, randomly defines variables for the weights and biases for each layer
    mu = 0
    sigma = 0.1

    # SOLUTION: Layer 1: Convolutional. Input = 32x32x1. Output = 28x28x6.
    conv1_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 1, 6), mean=mu, stddev=sigma))
    conv1_b = tf.Variable(tf.zeros(6))
    conv1 = tf.nn.conv2d(x, conv1_W, strides=[1, 1, 1, 1], padding='VALID') + conv1_b

    # SOLUTION: Activation.
    conv1 = tf.nn.relu(conv1)

    # SOLUTION: Pooling. Input = 28x28x6. Output = 14x14x6.
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # SOLUTION: Layer 2: Convolutional. Output = 10x10x16.
    conv2_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 6, 16), mean=mu, stddev=sigma))
    conv2_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(conv1, conv2_W, strides=[1, 1, 1, 1], padding='VALID') + conv2_b

    # SOLUTION: Activation.
    conv2 = tf.nn.relu(conv2)

    # SOLUTION: Pooling. Input = 10x10x16. Output = 5x5x16.
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # SOLUTION: Flatten. Input = 5x5x16. Output = 400.
    fc0 = flatten(conv2)

    # SOLUTION: Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_W = tf.Variable(tf.truncated_normal(shape=(400, 120), mean=mu, stddev=sigma))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1 = tf.matmul(fc0, fc1_W) + fc1_b

    # SOLUTION: Activation.
    fc1 = tf.nn.relu(fc1)

    # SOLUTION: Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_W = tf.Variable(tf.truncated_normal(shape=(120, 84), mean=mu, stddev=sigma))
    fc2_b = tf.Variable(tf.zeros(84))
    fc2 = tf.matmul(fc1, fc2_W) + fc2_b

    # SOLUTION: Activation.
    fc2 = tf.nn.relu(fc2)

    # SOLUTION: Layer 5: Fully Connected. Input = 84. Output = 42.
    fc3_W = tf.Variable(tf.truncated_normal(shape=(84, 42), mean=mu, stddev=sigma))
    fc3_b = tf.Variable(tf.zeros(42))
    logits = tf.matmul(fc2, fc3_W) + fc3_b

    return logits