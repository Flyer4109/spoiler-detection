import tensorflow as tf
import os
from sklearn.metrics import roc_auc_score

'''
Input in 61 time steps:
['this']    -> [1]
['is']      -> [2]
['a']       -> [3]
['unknown'] -> [8000]
['this']    -> [1]
['tweet']   -> [4]
['pad_token'] -> [0]
...         -> ...
['pad_token'] -> [0]

2 Outputs:
non-spoiler = [0, 1]
spoiler =  [1, 0]
'''

'''
OUR NEURAL NETWORK

'''


class Config:
    num_layers = 2
    num_epochs = 1
    num_classes = 2

    time_steps = 61

    batch_size = 32
    hidden_size = 200
    vocab_size = 8001
    embedding_size = 100

    learning_rate = 0.001


# Class for neural network
class RnnLstm:
    # Constructor. Takes number of inputs, number of outputs and batch size as arguments
    def __init__(self, config):
        self.config = config

        self.data_holder = tf.placeholder(tf.int32, [None, self.config.time_steps])
        self.targets_holder = tf.placeholder(tf.float32, [None, self.config.num_classes])

        # creates embedding vectors
        # e.g vocab_size = 2, embedding_size = 2 creates:
        # [
        #   [0.123, 0.456]
        #   [0.789, 0.111]
        # ]
        self.embeddings = tf.Variable(tf.random_uniform([self.config.vocab_size, self.config.embedding_size], -0.1, 0.1))

        self.lstm = tf.contrib.rnn.BasicLSTMCell(self.config.hidden_size, forget_bias=1)

        self.output_layer = {'weights': tf.Variable(tf.random_normal([self.config.hidden_size, self.config.num_classes])),
                             'biases': tf.Variable(tf.random_normal([self.config.num_classes]))}

    # method that runs the network with given input: data (tensor)
    def run_network(self, data):
        # Formula we use for each layer: (input_data * weights) + biases

        embedded_words = tf.nn.embedding_lookup(self.embeddings, data)

        final = tf.unstack(embedded_words, self.config.time_steps, 1)

        outputs, _ = tf.contrib.rnn.static_rnn(self.lstm, final, dtype=tf.float32)

        # matrix multiplication
        output = tf.matmul(outputs[-1], self.output_layer['weights']) + self.output_layer['biases']

        return output   # return output shape

    # method that trains the neural network with arguments: data (DataParser class), num_epochs (int)
    def train_network(self, data):
        # runs network
        scores = self.run_network(self.data_holder)

        predictions = tf.nn.softmax(scores)

        #auc = tf.metrics.auc(self.targets_holder, predictions)

        # this gets the total error (loss) between prediction and expectation
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=scores, labels=self.targets_holder))

        # Optimizer with learning_rate = 0.001
        optimizer = tf.train.AdamOptimizer().minimize(loss)

        # saver object to save the variables of the model
        # saver = tf.train.Saver()

        # starts a tensorflow session to run code
        with tf.Session() as sess:
            # initializes all tensorflow arguments
            init = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
            sess.run(init)

            # for loop that feeds the data into the neural network
            for epoch in range(self.config.num_epochs):
                epoch_loss = 0
                epoch_x, epoch_y = data.next_batch(self.config.batch_size)
                while not len(epoch_x) < self.config.batch_size:
                    # gets the next batch of train data and its corresponding expected value
                    epoch_x, epoch_y = data.next_batch(self.config.batch_size)

                    # turns epoch variables into tensors
                    train_x = sess.run(tf.constant(epoch_x))
                    train_y = sess.run(tf.constant(epoch_y))

                    # feed train_x and train_y into neural network and runs optimizer and cost
                    _, l = sess.run([optimizer, loss], feed_dict={self.data_holder: train_x, self.targets_holder: train_y})
                    epoch_loss += l

                data.reset_training_data()

                # to see training progress
                print('Epoch', epoch, 'completed out of', self.config.num_epochs, 'cost:', epoch_loss)

            # returns a 1D array with boolean values of the neural networks predictions
            # e.g. [True, False, True, True] this shows the neural network got 3 out of 4 correct
            correct = tf.equal(tf.argmax(predictions, 1), tf.argmax(self.targets_holder, 1))

            p = tf.argmax(predictions, 1)
            true_values = tf.argmax(self.targets_holder, 1)

            # works out the total accuracy of the correct variables by casting boolean variables to floats
            # e.g. [True, False, True, True] -> [1.0, 0.0, 1.0, 1.0] -> 0.75    Accuracy = 75%
            accuracy = tf.reduce_mean(tf.cast(correct, dtype=tf.float32))

            # gets test data from DataParser class to test accuracy
            epoch_x, epoch_y = data.get_test_data()
            test_x = sess.run(tf.constant(epoch_x))
            test_y = sess.run(tf.constant(epoch_y))

            # this evaluates (runs) the variable accuracy
            print('Accuracy:', accuracy.eval({self.data_holder: test_x, self.targets_holder: test_y}))

            # this evaluates (runs) the variable accuracy
            a, b = sess.run([true_values, p], feed_dict={self.data_holder: test_x, self.targets_holder: test_y})
            print('AUC score:', roc_auc_score(a, b))

            # this saves the current state of the model with filename "model.ckpt"
            # saver.save(sess, "./model.ckpt")

            return a, b

    # method to use network using saved model state
    # input is a 1D tensor which represents one line of data
    # e.g. [0.0045432, 0.0121313, 0.01213131, 0.16]
    def use_network(self, data):
        # tf.reset_default_graph()
        # saver object to restore model
        saver = tf.train.Saver()

        # this runs the network with given value
        prediction = self.run_network(self.data_holder)

        # starts a tensorflow session to run code
        with tf.Session() as sess:
            # initializes all tensorflow arguments
            tf.global_variables_initializer().run()

            # restores model, give path to file
            # dir_path = os.path.dirname(os.path.realpath(__file__))
            saver.restore(sess, "./model.ckpt")
            # convert array to tensor
            input_data = sess.run(tf.constant(data))
            # evaluate prediction and feed in input_data tensor
            array = sess.run(prediction, feed_dict={self.data_holder: input_data})

            # argmax() gets 1D array with the index of the maximum value
            # e.g. [3.3241341, 4.2313212] -> [1]
            # e.g. [6.2132131, 5.1231231] -> [0}
            result = sess.run(tf.argmax(array, 1))

        return result
