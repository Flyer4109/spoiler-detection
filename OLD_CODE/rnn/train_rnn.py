import rnn_lstm as rnn
import data_helper as dh
from sklearn.model_selection import KFold
import tensorflow as tf
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np
from scipy import interp
import matplotlib.pyplot as plt


def main():
    # creates a DataParser object using labelled data in trial_data.csv
    parser = dh.DataParser("../preprocess_data/tweet_data.csv")

    k_fold = KFold(n_splits=10, shuffle=True)
    split = k_fold.split(parser.get_data())

    k = 1

    tprs = []
    mean_fpr = np.linspace(0, 1, 100)
    mean_roc_score = []

    for train_index, test_index in split:
        print('K:', k)
        k += 1

        with tf.variable_scope(str(k)):
            # creates a neural network with 4 inputs, 2 outputs and batch_size of 10000
            network = rnn.RnnLstm(rnn.Config())

            parser.split_data(train_index, test_index)

            # train the neural network pass DataParser object and num_epoch=10
            true_values, predictions = network.train_network(parser)
            fpr, tpr, thresholds = roc_curve(true_values, predictions)
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            mean_roc_score.append(roc_auc_score(true_values, predictions))

    print('Average ROC AUC score:', np.mean(mean_roc_score))

    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', alpha=.8)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    plt.plot(mean_fpr, mean_tpr, color='b', lw=2, alpha=.8)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

    plt.savefig('roc_1.png')


if __name__ == '__main__':
    main()
