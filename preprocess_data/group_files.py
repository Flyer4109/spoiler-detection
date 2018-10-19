# This program combines the 40 labelled tweet files into one

import csv

# The file paths are given to the labelled tweets
FILE_NAME = "../data/labelled/set_b/labelled_tweet_data_set_B_"
FILE_NAME_2 = "../data/labelled/set_b/additional_tweets.csv"
FILE_NAME_3 = "../data/labelled/set_b/addtional_tweets_2.csv"
NUM_FILES = 40

# Write a file that contains all of 10,000 tweets
with open('tweet_data.csv', 'w') as final_file:
    writer = csv.writer(final_file)

    # Iterates through the labelled data files in set B
    for file_num in range(NUM_FILES):
        with open(FILE_NAME + str(file_num) + ".csv", 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                writer.writerow(row)

    # Adds additional found spoiler tweets collected
    with open(FILE_NAME_2, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            writer.writerow([row[0], 's'])

    # Adds additional found spoiler tweets collected
    with open(FILE_NAME_3, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            writer.writerow([row[0] + ' #gameofthrones', 's'])
