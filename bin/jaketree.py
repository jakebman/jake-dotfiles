#!/usr/bin/env python3

from fileinput import input
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv

def common_word_barrier(strings):
    prefix = commonprefix(strings)
    index = len(prefix)
    l=min(len(s) for s in strings)
    # if index == l: return prefix # no need to check deeper - they're either all the same, or one is exactly the common prefix

    # TODO: potentially find if the prefix is a barrier for some and not others?
    # Alternatively, figure out the last-enough barriers in each and pick the (one that is most common? last shared one? maximum?)
    matches = re.finditer('\\b', prefix)
    return list(matches)

DEFAULT_COMMON=common_word_barrier

def calc_args(argv):
    args = argparse.ArgumentParser(description='Remove common prefixes between lines of input. Works best on already-sorted input')
    args.add_argument("files", nargs="*") # default = none
    args.add_argument("--pathwise -p", action='store_const', dest='commonStrat', const=commonpath, help="only break on path separators")
    args.add_argument("--wordwise -w", action='store_const', dest='commonStrat', const=common_word_barrier, help="break on on a word barrier (default)")
    args.add_argument("--textwise -t", action='store_const', dest='commonStrat', const=commonprefix, help="recognize any text as the common prefix")
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

    if deserveElipsis(index, line):
        prefix = ' '*(index-3) + '...'
    else:
        prefix = ' ' * index
    print(prefix + line[index:])


def deserveElipsis(index, line):
    if index < 3: return False
    if index >= len(line): return False
    if '/' != line[index]: return True
    return False

def main():
    args = calc_args(sys.argv[1:])
    run_on_files(**args)

if __name__ == '__main__':
    try:
        main()
    except (BrokenPipeError, IOError):
        exit(55)
