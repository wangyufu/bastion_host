import tensorflow as tf
import numpy as np


def make_layer(inputs, in_size, out_size, activate=None):
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    basis = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    result = tf.matmul(inputs, weights) + basis
    if activate is None:
        return result
    else:
        return activate(result)


class BPNeuralNetwork:
    def __init__(self):
        self.session = tf.Session()
        self.input_layer = None
        self.label_layer = None
        self.loss = None
        self.optimizer = None
        self.layers = []

    def __del__(self):
        self.session.close()

    def train(self, cases, labels, limit=100, learn_rate=0.05):
        # 构建网络
        self.input_layer = tf.placeholder(tf.float32, [None, 2])
        self.label_layer = tf.placeholder(tf.float32, [None, 1])
        self.layers.append(make_layer(self.input_layer, 2, 10, activate=tf.nn.relu))
        self.layers.append(make_layer(self.layers[0], 10, 2, activate=None))
        self.loss = tf.reduce_mean(tf.reduce_sum(tf.square((self.label_layer - self.layers[1])), reduction_indices=[1]))
        self.optimizer = tf.train.GradientDescentOptimizer(learn_rate).minimize(self.loss)
        initer = tf.initialize_all_variables()
        # 做训练
        self.session.run(initer)
        for i in range(limit):
            self.session.run(self.optimizer, feed_dict={self.input_layer: cases, self.label_layer: labels})

    def predict(self, case):
        return self.session.run(self.layers[-1], feed_dict={self.input_layer: case})

    def test(self):
        x_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y_data = np.array([[0, 1, 1, 0]]).transpose()
        test_data = np.array([[0, 1]])
        self.train(x_data, y_data)
        print(self.predict(test_data))

nn = BPNeuralNetwork()
nn.test()
