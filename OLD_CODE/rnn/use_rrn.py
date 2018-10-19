import rnn_lstm as rnn
import data_helper as dh


def main():
    # creates a neural network with 4 inputs, 2 ouputs and batch_size of 10000
    network = rnn.RnnLstm(rnn.Config())

    # creates a DataParser object using labelled data in trial_data.csv
    parser = dh.DataParser("../preprocess_data/tweet_data.csv")

    tweets = ["I love the ice dragon", "Dany is so cool", "Littlefinger is dead!", "I love game of thrones",
              "NOOOOOO the white walkers are gonna bring the dead dragon back so it's on their side now. Fuckin' cunt this geezer is! #GameOfThrones"]

    #tweets = [parser.process(tweet) for tweet in tweets]

    for tweet in tweets:
        print(tweet)
        # if network.use_network([parser.process(tweet)])[0] == 0:
        #     print("This is a spoiler", end='\n\n')
        # elif network.use_network([parser.process(tweet)])[0] == 1:
        #     print("This is not a spoiler", end='\n\n')

        print(network.use_network([parser.process(tweet)]))

    # close file used in the parser
    parser.close_file()

if __name__ == '__main__':
    main()
