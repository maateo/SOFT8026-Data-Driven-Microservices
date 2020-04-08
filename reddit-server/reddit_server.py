import logging
import random
import time
from concurrent import futures

import grpc
import pandas as pd

import Assignment1_pb2
import Assignment1_pb2_grpc


class RedditServer(Assignment1_pb2_grpc.RedditServicer):

    def __init__(self):
        self.reddit_posts = pd.read_csv("r_dataisbeautiful_posts.csv", encoding="latin")

    def RequestRedditPosts(self, request, context):
        print("Received a request for %d reddit posts" % request.number_of_reddit_posts, flush=True)

        for _ in range(request.number_of_reddit_posts):
            random_post = self.reddit_posts.iloc[random.randint(1, self.reddit_posts.shape[0])]

            # TODO: Change the columns that we are getting
            response = Assignment1_pb2.RedditPostReply(
                id=str(random_post[0]),
                title=str(random_post[1]),
                score=str(random_post[2]),
                author=str(random_post[3]),
                full_link=str(random_post[4]),
                over_18=str(random_post[5])
            )

            time.sleep(1 / random.uniform(0.7, 3))  # Sleep for random amount, so number of reddit posts is anywhere between 1 and 3 per second, with mostly 2 per second

            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Assignment1_pb2_grpc.add_RedditServicer_to_server(RedditServer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
