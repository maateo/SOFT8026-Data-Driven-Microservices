#!/usr/bin/env python
import re


def get_word_and_vowel_count(event, context):
    word_count = len(re.findall(r'\w+', event["data"]))

    vowels = 'aeiou'
    vowel_count = 0

    for letter in event["data"].lower():
        if letter in vowels:
            vowel_count += 1

    return "{'word_count' : %d, 'vowel_count' : %d}" % (word_count, vowel_count)
