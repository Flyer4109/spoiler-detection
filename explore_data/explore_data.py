import re
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import matplotlib.pyplot as plt
import seaborn as sns

# file where tweet data is stored
FILE_NAME = "../preprocess_data/tweet_data.csv"
# size of vocabulary
VOCAB_SIZE = 5000
# regex to remove string that only contain punctuation e.g '!@*,.>\}{'
PUNCTUATION = r'^[!\"#$%&\'()*+,./:;<=>?@\\^_`{|}~\-\[\]£’…”“‘]+$'

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

# array that contains all words
all_words = []

# list of stopwords to filter out
STOPWORDS = set(stopwords.words('english')) - set(BLACKLIST_STOPWORDS)
longest_tweet = 0
spoiler_counter = 0
nonspoiler_counter = 0
tweet_lengths = []

with open(FILE_NAME, 'r', newline='') as file:
    reader = csv.reader(file)
    tweet_tok = TweetTokenizer()
    for row in reader:
        tweet = []
        words = tweet_tok.tokenize(row[0])
        for word in words:
            if word.lower() not in STOPWORDS:
                if not re.match(PUNCTUATION, word.lower()):
                    if word.lower() in CONTRACTIONS:
                        # print("contraction changing:", word, 'to', CONTRACTIONS[word.lower()])
                        for expanded_word in word_tokenize(CONTRACTIONS[word.lower()]):
                            # add lowercase version of word to all_words array
                            if expanded_word not in STOPWORDS:
                                print("Success!")
                                tweet.append(expanded_word)
                            else:
                                print('removing:', expanded_word)
                    else:
                        tweet.append(word.lower())
        if len(tweet) > longest_tweet:
            longest_tweet = len(tweet)

        tweet_lengths.append(len(tweet))

        if row[1] == 's':
            spoiler_counter += 1
        elif row[1] == 'ns':
            nonspoiler_counter += 1
        else:
            print("target:", row[1])

print('longest tweet:', longest_tweet)
print('average tweets:', sum(tweet_lengths)/len(tweet_lengths))
print('spoilers:', spoiler_counter)
print('non-spoilers:', nonspoiler_counter)

plt.figure(figsize=(10,5))
plt.xlim([0.0, 61])
plt.ylim([0.0, 0.09])
plt.xlabel('Tweet length')
plt.title('Distribution of Tweet Lengths')
sns.distplot(tweet_lengths, color='g')
plt.show()