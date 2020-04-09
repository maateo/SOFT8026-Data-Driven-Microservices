from __future__ import print_function

import datetime
import logging
import random
import re

import grpc
import redis

import Assignment1_pb2
import Assignment1_pb2_grpc


def run():
    with grpc.insecure_channel('reddit_post_server:50052') as channel:
        stub = Assignment1_pb2_grpc.RedditStub(channel)

        while True:
            for reddit_post in stub.RequestRedditPosts(Assignment1_pb2.RedditPostRequest(number_of_reddit_posts=random.randint(1, 15))):
                try:
                    conn = redis.StrictRedis(host='redis', port=6379)
                    reddit_post_data = {
                        "id": str(reddit_post.id),
                        "title": str(reddit_post.title),
                        "score": str(reddit_post.score),
                        "author": str(reddit_post.author),
                        "original_date": str(reddit_post.original_date),
                        "full_link": str(reddit_post.full_link),
                        "over_18": str(reddit_post.over_18),
                        # "word_count": str(len(re.findall(r'\w+', reddit_post.text))),
                        "time_analysed": str(datetime.datetime.now())
                    }

                    # conn.hmset("reddit_posts." + str(datetime.datetime.now()), reddit_post_data)
                    # conn.set("reddit_posts_3md." + str(datetime.datetime.now()), reddit_post.target, ex=180)
                    #
                    # analise_totals(conn, reddit_post.text)
                    # analise_most_of(conn, reddit_post.text)
                    # analise_last_3_minutes(conn)

                except Exception as ex:
                    print('Error:', ex)

                print("Reddit analysis client received: ", reddit_post.id, reddit_post.title, reddit_post.score, reddit_post.author, reddit_post.original_date, reddit_post.full_link, reddit_post.over_18, flush=True)


def analise_totals(conn, text):
    word_count = len(re.findall(r'\w+', text))

    vowels = 'aeiou'
    vowel_count = 0

    for letter in text.lower():
        if letter in vowels:
            vowel_count += 1

    conn.incrby("reddit_posts_total_vowel_count", vowel_count)
    conn.incrby("reddit_posts_total_word_count", word_count)


def analise_last_3_minutes(conn):
    keys = conn.scan_iter("reddit_posts_3md*")
    sentiments = [0, 0, 0, 0, 0]

    for key in keys:
        target = int(conn.get(key))
        sentiments[target] += 1

    conn.set("reddit_posts_3_minute_sentiment", str(sentiments))


def analise_most_of(conn, text):
    word_count = len(re.findall(r'\w+', text))

    ath_word_count = conn.get("reddit_posts_all_time_high_word_count")

    if ath_word_count is None or word_count > int(ath_word_count):
        conn.set("reddit_posts_all_time_high_word_count", word_count)
        conn.set("reddit_posts_all_time_high_word", text)


if __name__ == '__main__':
    logging.basicConfig()
    run()
