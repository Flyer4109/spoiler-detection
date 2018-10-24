# Spoiler detection in _Game of Thrones_ tweets

This project used a Long Short-Term Memory network to detect 'spoilers' in Twitter tweets from
the TV show _Game of Thrones_. A 'spoiler' for this project is defined as follows: 'a Twitter
tweet which reveals unknown information about the storyline of _Game of Thrones_ after Season 7
Episode 3'. Using 10 fold cross-validation gave a f1-score of 0.7597 and
recall of 0.710.To use the trained LSTM run `use_rnn.py` found in the 'rnn' directory.

Tweets were:
* Collected using Tweepy as seen in `collect_data`.
* Labelled using a website as seen in `label_data`.
* Preprocessed using NLP techniques as seen in `preprocess_data`.
* Explored as seen in `explore_data`.

This project used:
* Python 3.6.3
* JavaScript
* HTML
* CSS

Python dependencies used:
* Tweepy 3.5.0
* NLTK 3.2.5
* Matplotlib 2.1.2
* seaborn 0.8.1
* pandas 0.22.0
* scipy 1.0.0
* numpy 1.14.1
* Keras 2.1.5
* TensorFlow 1.5
* flask 0.12.2
* scikit-learn 0.19.1

These dependencies were all installed using pip. If I have missed any dependencies just install
them using pip.

OLD_CODE contains the TensorFlow version of this project but was later replaced by Keras.



