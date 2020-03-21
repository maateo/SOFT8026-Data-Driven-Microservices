import logging
import random
import time
from concurrent import futures

import grpc
import pandas as pd

import Assignment1_pb2
import Assignment1_pb2_grpc


class TweetServer(Assignment1_pb2_grpc.TweetServicer):

    def __init__(self):
        self.tweets = pd.read_csv("training.1600000.processed.noemoticon.csv", encoding="latin")

    def RequestTweets(self, request, context):
        print("Received a request for %d tweets" % request.number_of_tweets, flush=True)

        for _ in range(request.number_of_tweets):
            random_tweet = self.tweets.iloc[random.randint(0, self.tweets.shape[0])]

            response = Assignment1_pb2.TweetReply(
                target=str(random_tweet[0]),
                id=str(random_tweet[1]),
                date=str(random_tweet[2]),
                flag=str(random_tweet[3]),
                user=str(random_tweet[4]),
                text=str(random_tweet[5])
            )

            time.sleep(1 / random.uniform(0.7, 3))  # Sleep for random amount, so number of tweets is anywhere between 1 and 3 per second, with mostly 2 per second

            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Assignment1_pb2_grpc.add_TweetServicer_to_server(TweetServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
