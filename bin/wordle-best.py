#! /bin/env python3

from collections import defaultdict

def squared_sum(it):
    return sum(i*i for i in it)

def score(word, by_key, target):
            # each non-unique word gets a large score
    return squared_sum(target - len(by_key.get(letter)) for letter in set(word)) + \
            (target*target * (len(word) - len(set(word)) ))
def explain_score(word, by_key):
    return {letter:len(by_key.get(letter)) for letter in word}

def main(words):
    """
        given a set of words on stdin, print the best wordle guess from them
    """
    by_key = defaultdict(set)
    for word in words:
        for letter in word:
            by_key[letter].add(word)

    target = len(words)/2
    print("target score is", target)
    for word in sorted(words, key=lambda word: score(word, by_key, target)):
        try:
            print(word, score(word, by_key, target), explain_score(word, by_key))
        except BrokenPipeError:
            # got cut off by something like `head`. Don't be bothered by it
            return



def get_words():
    words=[]
    try:
        while True:
            words.append(input())
    except EOFError:
        return words


if __name__ == "__main__":
    main(get_words())
