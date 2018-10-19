import re
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer


# file where tweet data is stored
FILE_NAME = "./tweet_data.csv"
# size of vocabulary
VOCAB_SIZE = 5000
# regex to remove string that only contain punctuation e.g '!@*,.>\}{'
PUNCTUATION = r'^[!\"#$%&\'()*+,./:;<=>?@\\^_`{|}~\-\[\]£’…”“‘]+$'
# maximum number of valid tokens in tweet
MAX_TWEET_LENGTH = 61
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

# list that will contain every encountered word in tweet data
all_words = []

# open data file and read tweets for processing
with open(FILE_NAME, 'r', newline='') as file:
    reader = csv.reader(file)
    # special tokenizer for tweets
    tweet_tok = TweetTokenizer()
    for row in reader:
        # stores amount of valid tokens in current tweet
        tweet_length = 0
        # array of words in tweet
        words = tweet_tok.tokenize(row[0])
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
                                all_words.append(expanded_word)
                                tweet_length += 1
                    else:
                        # add lowercase version of word to all_words array
                        all_words.append(word.lower())
                        tweet_length += 1

        # calculate number of padding to add
        num_padding = MAX_TWEET_LENGTH - tweet_length
        # add PAD_TOKEN num_padding amount of times to add_words
        all_words += [PAD_TOKEN] * num_padding

# get frequency distribution of all the words
all_words = nltk.FreqDist(all_words)

# get the VOCAB_SIZE most common words
vocabulary_keys = [word[0] for word in all_words.most_common(VOCAB_SIZE - 1)]

# add UNKNOWN_TOKEN
vocabulary_keys.append(UNKNOWN_TOKEN)

# enumerate vocabulary_keys and create a dictionary where the lower the index the more popular the key is
# e.g {'pad_token' : 0, '#gameofthrones' : 1, ... , 'unknown_token' : VOCAB_SIZE + 1}
vocabulary = {word: index for index, word in enumerate(vocabulary_keys)}

# write a csv file that contains the vocabulary
# and where each line has the word,index
with open('vocabulary.csv', 'w') as file:
    writer = csv.writer(file)
    for word, index in vocabulary.items():
        writer.writerow([word, index])
