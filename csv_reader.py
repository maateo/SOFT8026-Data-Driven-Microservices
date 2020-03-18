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
"""The Python implementation of the GRPC helloworld.Greeter client."""
import time

import grpc

import csv
import random
import pandas as pd

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    tweets = pd.read_csv("sentiment140/training.1600000.processed.noemoticon.csv", header=None, encoding="latin")
    tweet = tweets.iloc[[random.randint(0, tweets.shape[0])]]
    print(tweet[5])

    print("BBBBBBBBBBBBBBB")
    tweet5 = tweet[5].values[0]
    print(tweet5)
    print("BBBBBBBBBBBBBBB")

    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(str(tweet[0].values[0]),)
    print(str(tweet[1].values[0]),)
    print(str(tweet[2].values[0]),)
    print(str(tweet[3].values[0]),)
    print(str(tweet[4].values[0]),)
    print(str(tweet[5].values[0]),)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print()


    print(tweet)
    print("bye")
# while True:
    #
    #     # with open("sentiment140/training.1600000.processed.noemoticon.csv", "r") as f:
    #     #     reader = csv.reader(f, delimiter=",")
    #     #     for i, line in enumerate(reader):
    #     #         print(i, " ", line)
    #     #
    #     #         sleep_duration = 1 / random.uniform(0.7, 3)
    #     #         print("sleeping for:" , sleep_duration)
    #     #         print()
    #     #         # time.sleep(sleep_duration)
    #     #         # print( 'line[{}] = {}'.format(i, line))
    #
    #     print(tweets.iloc[random.randint(0, tweets.shape[0] )])
    #     print()
    #     print()
    #     print()
    #
    #     # with grpc.insecure_channel('greeter_server:50051') as channel:
    #     #     stub = helloworld_pb2_grpc.GreeterStub(channel)
    #     #     total_length = 0
    #     #     for response in stub.SayHello(helloworld_pb2.HelloRequest(name='Larkin')):
    #     #         total_length += len(response.message)
    #     #         print("real-time character count: " + str(total_length))
    #     #         print("Greeter client received: " + response.message, flush=True)
    #     #         time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    run()
