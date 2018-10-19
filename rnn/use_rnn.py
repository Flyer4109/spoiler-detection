#!flask/bin/python

from keras.models import load_model
import numpy as np
import data_helper as dh
from flask import Flask, render_template, request, redirect, Response
import random, json
import sys

app = Flask(__name__)

# Flask uses URL as a way to point to methods
# This program creats a local server and host the html in template


@app.route('/')
def html():
    return render_template('tweet_detector.html')

# Main program to use the RNN LSTM

@app.route("/main", methods=['POST'])
def main():
    # data helper is used to preprocess the data
    parser = dh.DataParser("../preprocess_data/tweet_data.csv")

    # load the best trained model
    model = load_model('best_model2.h5')

    # get the tweet from the user
    data = request.get_json(force=True)

    tweet = data

    # input tweet into array and prediction is recieved
    prediction = model.predict(np.array([parser.process(tweet)]))

    # prediction is returned to user
    if prediction[0][0] > prediction[0][1]:
        return 'spoiler'
    else:
        return 'nonspoiler'

if __name__ == '__main__':
    app.run()
