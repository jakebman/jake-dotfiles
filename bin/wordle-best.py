#! /bin/env python3

from collections import defaultdict

def squared_sum(it):
    return sum(i*i for i in it)

def score(word, by_key, target):
    return squared_sum(target - len(by_key.get(letter)) for letter in word)

def explain_score(word, by_key):
    return {letter:len(by_key.get(letter)) for letter in word}

def main(words):
    """
        given a set of words on stdin, print the best wordle guess from them
    """
    print(words)
    by_key = defaultdict(set)
    for word in words:
        for letter in word:
            by_key[letter].add(word)

    for word in sorted(words, key=lambda word: score(word, by_key, len(words)/2)):
        print(word, score(word, by_key, len(words)/2), explain_score(word, by_key))



def get_words():
    words=[]
    try:
        while True:
            words.append(input())
    except EOFError:
        return words


if __name__ == "__main__":
    main(get_words())
