import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
import data_helper as dh
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, f1_score, recall_score, roc_curve
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from keras.callbacks import EarlyStopping
from scipy import interp

# creates a DataParser object using labelled data in trial_data.csv
parser = dh.DataParser("../preprocess_data/tweet_data.csv")

# creates the indices for spliting the data into training and testing
k_fold = KFold(n_splits=10, shuffle=True)
split = k_fold.split(parser.get_data())

#arrays to maintain averages from the cross validation
auc_averages = []
f1_averages = []
recall_averages = []

train = pd.DataFrame()
val = pd.DataFrame()

count = 0

tprs = []
mean_fpr = np.linspace(0, 1, 100)

for train_index, test_index in split:
    parser.split_data(train_index, test_index)

    (X_train, y_train), (X_test, y_test) = parser.get_splits()

    # create the model
    embedding_vector_length = 100
    model = Sequential()
    model.add(Embedding(5000, embedding_vector_length, input_length=32))
    model.add(LSTM(32))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    # Early stop can be used if desired
    # call_back = EarlyStopping()
    history = model.fit(np.array(X_train), np.array(y_train), epochs=5, batch_size=64, validation_split=0.1)

    train[str(count)] = history.history['loss']
    val[str(count)] = history.history['val_loss']

    # shows validaiton and training loss on a graph
    plt.plot(train[str(count)])
    plt.plot(val[str(count)])
    plt.title('model train vs validation loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper right')
    plt.show()

    count += 1

    scores = model.evaluate(np.array(X_test), np.array(y_test), verbose=1)

    predictions = model.predict_proba(np.array(X_test))

    y = []
    p = []
    for i in y_test:
        if i[0] < i[1]:
            y.append(0)
        else:
            y.append(1)

    for i in predictions:
        if i[0] < i[1]:
            p.append(0)
        else:
            p.append(1)

    fpr, tpr, thresholds = roc_curve(y, p)
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0

    auc_score = roc_auc_score(np.array(y_test), predictions)
    f_score = f1_score(y, p)
    r_score = recall_score(y, p)

    auc_averages.append(auc_score)
    if f_score != 0:
        f1_averages.append(f_score)
    if r_score != 0:
        recall_averages.append(r_score)

    print('roc_auc score:', auc_score)
    print('f1 score:', f_score)
    print('recall score:', r_score)
    print("Accuracy: %.2f%%" % (scores[1]*100))

    # model.save('best_model_'+str(count)+'.h5') this is used to save a model

print('Mean auc:', np.mean(auc_averages))
print('Mean f1:', np.mean(f1_averages))
print('Mean recall:', np.mean(recall_averages))

# code to print the roc curve
# mean_tpr = np.mean(tprs, axis=0)
# mean_tpr[-1] = 1.0
# plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', alpha=.8)
# plt.plot(mean_fpr, mean_tpr, color='b', lw=2, alpha=.8)
# plt.xlim([-0.05, 1.05])
# plt.ylim([-0.05, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.show()
#
# blue_patch = mpatches.Patch(color='blue', label='train')
# orange_patch = mpatches.Patch(color='orange', label='val')
#
# # Final evaluation of the model
# plt.plot(train, color='b')
# plt.plot(val, color='orange')
# plt.title('model train vs validation loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend(handles=[blue_patch, orange_patch], loc='upper right')
# plt.show()
