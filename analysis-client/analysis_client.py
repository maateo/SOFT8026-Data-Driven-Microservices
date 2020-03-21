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
        with grpc.insecure_channel('tweet_server:50051') as channel:
            stub = Assignment1_pb2_grpc.TweetStub(channel)
            # response = stub.RequestATweet(Assignment1_pb2.TweetRequest())

            for tweet in stub.RequestATweet(Assignment1_pb2.TweetRequest()):
                try:
                    conn = redis.StrictRedis(host='redis', port=6379)
                    tweet_data = {
                        "target": str(tweet.target),
                        "id": str(tweet.id),
                        "date": str(tweet.date),
                        "flag": str(tweet.flag),
                        "user": str(tweet.user),
                        "text": str(tweet.text),
                        "word_count": str(len(re.findall(r'\w+', tweet.text))),
                        "time_analysed": str(datetime.datetime.now())
                    }

                    conn.hmset("tweets." + str(datetime.datetime.now()), tweet_data)
                    conn.set("3md." + str(datetime.datetime.now()), tweet.target, ex=180)

                    analise_totals(conn, tweet.text)
                    analise_most_of(conn, tweet.text)
                    analise_last_3_minutes(conn)

                except Exception as ex:
                    print('Error:', ex)

                print("Analysis client received: ", tweet.target, tweet.id, tweet.date, tweet.flag, tweet.user, tweet.text, flush=True)
                time.sleep(1 / random.uniform(0.7, 3))  # Sleep for random amount, so number of tweets is anywhere between 1 and 3 per second, with mostly 2 per second


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
