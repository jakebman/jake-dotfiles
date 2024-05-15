#! /bin/env python3


def pad(word):
    """
        If a word starts or ends with a dot, pad the other side with dots
    """
    if len(word) >= 5 or len(word) < 1:
        return word # no padding
    if word[0] == "-": # do not modify flags... ever!
        return word
    if word[0] == ".":
        return word.ljust(5, '.')
    if word[-1] == ".":
        return word.rjust(5, '.')
    return word


def main(words):
    """
        given a set of words on stdin, do padding on each
    """
    for word in words:
        print(pad(word))

def get_words():
    try:
        while True:
            yield input()
    except EOFError:
        pass # or return


if __name__ == "__main__":
    main(get_words())
