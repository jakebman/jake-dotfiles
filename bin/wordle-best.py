#! /bin/env python3


def main(words):
    """
        given a set of words on stdin, print the best wordle guess from them
    """
    print(words)

def get_words():
    words=[]
    try:
        while True:
            words.append(input())
    except EOFError:
        return words


if __name__ == "__main__":
    main()
