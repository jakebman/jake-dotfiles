#!/usr/bin/env python3

from fileinput import input
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv

BARRIER=re.compile('\\b')
def common_word_barrier(strings):
    prefix = commonprefix(strings)
    index = len(prefix)
    l=min(len(s) for s in strings)
    # if index == l: return prefix # no need to check deeper - they're either all the same, or one is exactly the common prefix

    # TODO: potentially find if the prefix is a barrier for some and not others?
    # Alternatively, figure out the last-enough barriers in each and pick the (one that is most common? last shared one? maximum?)
    split=0
    for string in strings:
        for match in BARRIER.finditer(string, 0, index):
            split = max(split, match.start())
    #split = max(match.start() for match in re.finditer('\\b', string) for string in strings if match.start() <= index)

    return prefix[:split]

DEFAULT_COMMON=common_word_barrier

def calc_args(argv):
    args = argparse.ArgumentParser(description='Remove common prefixes between lines of input. Works best on already-sorted input')
    args.add_argument("files", nargs="*") # default = none
    group = args.add_mutually_exclusive_group()
    group.add_argument("--wordwise", "-w", action='store_const', dest='commonStrat', const=common_word_barrier, help="break on on a word barrier (default)")
    group.add_argument("--pathwise", "-p", action='store_const', dest='commonStrat', const=commonpath, help="only break on path separators")
    group.add_argument("--textwise", "-t", action='store_const', dest='commonStrat', const=commonprefix, help="recognize any text as the common prefix")
    args.set_defaults(commonStrat=DEFAULT_COMMON)
    out = args.parse_args(argv)
    return out.__dict__

def run_on_files(files=None, commonStrat=DEFAULT_COMMON):
    with input(files=files) as stdin:
        run(stdin, commonStrat=commonStrat)

def run(stdin, commonStrat=DEFAULT_COMMON):
    prev=''
    for line in stdin:
        line = line.strip()
        do_line(prev, line, commonStrat=DEFAULT_COMMON)
        prev = line


def do_line(prev, line, commonStrat=DEFAULT_COMMON):
    prefix = commonStrat([line, prev])
    index = len(prefix) # with commonpath, this is stopped BEFORE the common slash
    paranoia = commonprefix([line[index:], prev[index:]])

    if index >= 5:
        prefix = ' '*(index-5) + '[...]'
    else:
        prefix = ' ' * index
    print(prefix + line[index:])


def main():
    args = calc_args(sys.argv[1:])
    run_on_files(**args)

if __name__ == '__main__':
    try:
        main()
    except (BrokenPipeError, IOError):
        exit(55)
