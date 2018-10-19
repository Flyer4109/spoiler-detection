# Created by Isao Ramos
# Program that connects to Twitter API using python module tweepy
# Then creates 40 files of data each containing 250 tweets each
# Each tweet has its retweets and links removed
# Program ignores duplicate tweets

import tweepy
import csv
from hashlib import sha256
import re

# Number of tweets per csv file
NUM_TWEETS_PER_FILE = 250

# Number of data csv files needed
MAX_NUM_DATA_FILES = 10000/NUM_TWEETS_PER_FILE

# Tokens and secrets for authentication for the Twitter API
# These tokens were removed as they meant to be kept secret
consumer_token = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

# Authenticates with the Twitter API
auth = tweepy.AppAuthHandler(consumer_token, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# Gets tweepy api wrapper
# Sleep for 15 minutes because of the Twitter API rate limit
# setting wait_on_rate_limit to True will make the program sleep automatically to avoid exceeding rate limits
api = tweepy.API(auth, wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

# Stores hashes of all received tweets in a set to ensure there are no duplicates
tweet_hash_set = set()

# Stores the file number we are currently working with
file_num = 0

# Stores number of tweets collected
tweet_count = 0

# Stores number of tweets collect for the current file
file_tweet_count = 0

# Opens a file with name of "tweet_data_<file_num>" in writing mode
csv_file = open("tweet_data_set_B_" + str(file_num) + ".csv", 'w')
# Store writer object for csv file
writer = csv.writer(csv_file)

# Stores the tweet id of the latest tweet
max_id = -1

# While loop until the program finishes writing the max number of files
while file_num < MAX_NUM_DATA_FILES:
    # Store tweets processed in this iteration for debugging
    tweets_processed = 0
    # Uses search API to get tweets with hash tag "gameofthrones" in english
    # Gets 100 tweets that have tweet id less than max_id inclusive
    tweets = api.search(q="#gameofthrones", lang="en", max_id=str(max_id - 1), count=100, tweet_mode="extended")
    # Avoids error when array is length 0
    if len(tweets) > 0:
        max_id = tweets[-1].id

    # Iterates through 100 tweets
    for tweet in tweets:
        # check if it is a retweet and if it is get the text
        if 'retweeted_status' in dir(tweet):
            text = tweet.retweeted_status.full_text
        else:
            text = tweet.full_text

        tweets_processed += 1
        # Hash tweet into hex
        hash_object = sha256(bytes(text, 'utf-8'))
        hex_dig = hash_object.hexdigest()

        # If statement that deals with tweet duplicates
        if hex_dig in tweet_hash_set:
            # If the tweet hash is in the set then skip tweet by continuing
            continue
        else:
            # Else the tweet hash is not in the set then it is a new tweet
            # If the number of tweets for the current file has reached 450 open a new file
            if file_tweet_count == NUM_TWEETS_PER_FILE:
                # Output progress
                print("\nFile", file_num, "was written with", file_tweet_count, "tweets")

                # Reset current file tweet counter
                file_tweet_count = 0

                # Increment file number
                file_num += 1

                # Close file and open a new one
                csv_file.close()
                csv_file = open("tweet_data_set_B_" + str(file_num) + ".csv", 'w')
                writer = csv.writer(csv_file)

            # Add tweet hash to set so no duplicates are added
            tweet_hash_set.add(hex_dig)

            # Modify tweet by removing https:t.co/ links
            tweet_without_links = re.sub(r'https://t\.co/[a-zA-Z0-9]+', r'', text)

            # Modify tweet by removing retweets "RE @user:"
            tweet_string = re.sub(r'RT @[^:]+:', r'', tweet_without_links)

            # Write tweet to current csv file
            writer.writerow([tweet_string])

            # Increment total tweet count and current file tweet count
            tweet_count += 1
            file_tweet_count += 1

    # Print out current status
    print("\nCurrent file tweet count:", file_tweet_count)
    print("Tweets processed this iteration:", tweets_processed)
    print("Current total tweet count:", tweet_count)

# Close csv file
csv_file.close()

# Output that the gathering of data has finished
print("\nCompleted getting data. Total amount of tweets collected:", tweet_count)


