import re
import csv
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

# regex to remove string that only contain punctuation e.g '!@*,.>\}{'
PUNCTUATION = r'^[!\"#$%&\'()*+,./:;<=>?@\\^_`{|}~\-\[\]£’…”“‘]+$'
# maximum number of valid tokens in tweet
MAX_TWEET_LENGTH = 32
# token used for words not in vocab
UNKNOWN_TOKEN = 'unknown_token'
# token used for padding
PAD_TOKEN = 'pad_token'

# blacklist of stopwords
BLACKLIST_STOPWORDS = ["you'll", "you'd", "that'll", "until", "while", "before", "after", "then", "once", "when", "not",
                       "no", "will", "don", "don't", "should", "should've", "now", 'ain', "once", 'aren', "aren't",
                       'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
                       'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
                       "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                       "won't", 'wouldn', "wouldn't"]

# dictionary of possible contractions and there corresponding expanded version
CONTRACTIONS = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

# list of stopwords to filter out
STOPWORDS = set(stopwords.words('english')) - set(BLACKLIST_STOPWORDS)


# class to parser train data for the neural network
class DataParser:
    def __init__(self, file_name):
        self.data = self.load_data(file_name)

        self.vocabulary = self.get_vocab()

        self.train_index = []
        self.test_index = []

        self.train_data_iterator = zip([0])
        self.train_targets_iterator = zip([0])
        self.test_data_iterator = zip([0])
        self.test_targets_iterator = zip([0])

    @staticmethod
    def load_data(file_name):
        data = pd.read_csv(file_name, header=None, names=['tweets', 'class'], dtype={'tweets': str, 'class': str})
        data = data.sample(frac=1).reset_index(drop=True)
        return data

    @staticmethod
    def get_vocab():
        vocabulary = dict()
        with open('../preprocess_data/vocabulary.csv', 'r', newline='', encoding='utf8') as vocab_file:
            reader = csv.reader(vocab_file)
            for row in reader:
                vocabulary[row[0]] = int(row[1])

        return vocabulary

    def split_data(self, train_index, test_index):
        self.train_index = train_index
        self.test_index = test_index
        self.reset_training_data()

    def reset_training_data(self):
        self.train_data_iterator = self.data['tweets'][self.train_index].iteritems()
        self.train_targets_iterator = self.data['class'][self.train_index].iteritems()

        self.test_data_iterator = self.data['tweets'][self.test_index].iteritems()
        self.test_targets_iterator = self.data['class'][self.test_index].iteritems()

    # gets the next batch of size batch_size
    def next_batch(self, batch_size):
        train_data_batch = []
        train_targets_batch = []
        for _ in range(batch_size):
            try:
                tweet = next(self.train_data_iterator)[1]
                target = next(self.train_targets_iterator)[1]
                train_data_batch.append(self.process(tweet))
                train_targets_batch.append(self.process_target(target))
            except StopIteration:
                break

        return train_data_batch, train_targets_batch

    def process(self, tweet):
        clean_tweet = []
        # special tokenizer for tweets
        tweet_tok = TweetTokenizer()
        # array of words in tweet
        words = tweet_tok.tokenize(tweet)
        # for every word in tweet remove stopwords, punctuation and expand contractions
        for word in words:
            if word.lower() not in STOPWORDS:
                if not re.match(PUNCTUATION, word.lower()):
                    if word.lower() in CONTRACTIONS:
                        # expand contractions using dictionary
                        for expanded_word in word_tokenize(CONTRACTIONS[word.lower()]):
                            # check if expanded word is a stop word
                            if expanded_word not in STOPWORDS:
                                # add lowercase version of word to all_words array
                                clean_tweet.append(expanded_word)
                    else:
                        # add lowercase version of word to all_words array
                        clean_tweet.append(word.lower())

        # calculate number of padding to add
        num_padding = MAX_TWEET_LENGTH - len(clean_tweet)

        if num_padding >= 0:
            # add PAD_TOKEN num_padding amount of times to add_words
            clean_tweet += [PAD_TOKEN] * num_padding
        else:
            clean_tweet = clean_tweet[0:MAX_TWEET_LENGTH]

        return self.encode(clean_tweet)

    def encode(self, tweet):
        encoded_tweet = []
        for word in tweet:
            if word in self.vocabulary:
                encoded_tweet.append(self.vocabulary[word])
            else:
                encoded_tweet.append(self.vocabulary[UNKNOWN_TOKEN])

        return encoded_tweet

    @staticmethod
    def process_target(target):
        # non-spoiler is [0, 1] and spoiler is [1, 0]
        if target == "ns":
            return [0, 1]
        else:
            return [1, 0]

    # method to get the test data to test accuracy of neural network
    def get_test_data(self):
        test_data_batch = []
        test_targets_batch = []

        for index, tweet in self.test_data_iterator:
            test_data_batch.append(self.process(tweet))

        for index, target in self.test_targets_iterator:
            test_targets_batch.append(self.process_target(target))

        return test_data_batch, test_targets_batch

    def get_data(self):
        return self.data

    def get_splits(self):
        train_data = []
        train_targets = []
        test_data = []
        test_targets = []

        for tweet in self.data['tweets'][self.train_index].tolist():
            train_data.append(self.process(tweet))

        for target in self.data['class'][self.train_index].tolist():
            train_targets.append(self.process_target(target))

        for tweet in self.data['tweets'][self.test_index].tolist():
            test_data.append(self.process(tweet))

        for target in self.data['class'][self.test_index].tolist():
            test_targets.append(self.process_target(target))

        return (train_data, train_targets), (test_data, test_targets)
