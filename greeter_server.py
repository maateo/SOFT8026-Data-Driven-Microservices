# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""
import random
from concurrent import futures
import datetime
import logging

import grpc

import Assignment1_pb2
import Assignment1_pb2_grpc

import redis

import time

import csv
import pandas as pd


# THIS  FILE IOS RESOPNSIBLE for sending back a line of tweets when requested

class Greeter(Assignment1_pb2_grpc.GreeterServicer):

    def __init__(self):
        self.tweets = pd.read_csv("sentiment140/training.1600000.processed.noemoticon.csv", encoding="latin")

    def SayHello(self, request, context):
        random_tweet = self.tweets.iloc[random.randint(0, self.tweets.shape[0])]

        response = Assignment1_pb2.HelloReply(
            target=str(random_tweet[0]),
            id=str(random_tweet[1]),
            date=str(random_tweet[2]),
            flag=str(random_tweet[3]),
            user=str(random_tweet[4]),
            text=str(random_tweet[5])
        )

        return response  # Generator


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Assignment1_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
