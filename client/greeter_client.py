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

from __future__ import print_function

import datetime
import logging
import random
import re
import time

import grpc
import redis

import Assignment1_pb2
import Assignment1_pb2_grpc


def run():
    while True:
        with grpc.insecure_channel('greeter_server:50051') as channel:
            stub = Assignment1_pb2_grpc.GreeterStub(channel)
            total_length = 0
            response = stub.SayHello(Assignment1_pb2.HelloRequest(name='Larkin'))
            # total_length += len(response.message)
            # print("real-time character count: " + str(total_length))

        try:
            conn = redis.StrictRedis(host='redis', port=6379)
            tweet_data = {
                "target": str(response.target),
                "id": str(response.id),
                "date": str(response.date),
                "flag": str(response.flag),
                "user": str(response.user),
                "text": str(response.text),
                "word_length": str(len(re.findall(r'\w+', response.text)))
            }

            conn.hmset("tweets." + str(datetime.datetime.now()), tweet_data)
            conn.set("3md." + str(datetime.datetime.now()), response.target, ex=180)

            analise_totals(conn, response.text)
            analise_most_of(conn, response.text)
            analise_last_3_minutes(conn)


        except Exception as ex:
            print('Error:', ex)

        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print("Greeter client received: ", response.target, response.id, response.date, response.flag, response.user, response.text, flush=True)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print()
        print()
        print()
        print()
        print()
        print()
        time.sleep(random.randint(1, 3))


def analise_totals(conn, text):
    word_count = len(re.findall(r'\w+', text))

    vowels = 'aeiou'
    vowel_count = 0

    for letter in text.lower():
        if letter in vowels:
            vowel_count += 1

    conn.incrby("total_vowel_count", vowel_count)
    conn.incrby("total_word_count", word_count)


def analise_last_3_minutes(conn):
    keys = conn.scan_iter("3md*")
    sentiments = [0, 0, 0, 0, 0]

    for key in keys:
        target = int(conn.get(key))
        sentiments[target] += 1

    conn.set("3_minute_sentiment", str(sentiments))

def analise_most_of(conn, text):
    word_count = len(re.findall(r'\w+', text))

    ath_word_count = conn.get("all_time_high_word_count")

    if ath_word_count is None or word_count > int(ath_word_count):
        conn.set("all_time_high_word_count", word_count)
        conn.set("all_time_high_word", text)


if __name__ == '__main__':
    logging.basicConfig()
    run()
