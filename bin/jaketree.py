#!/usr/bin/env python3

from fileinput import input as fileinput
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv

# r'\b', but only at the end of words - a \word character followed by a non-\Word character or eol
BARRIER=re.compile(r'(?<=\w)(?=\W|$)')
ELISION_MARKER='...'

def index_of_lowest_element(items):
    lowest = min(items)
    return items.index(lowest)


def common_word_barrier(strings):
    prefix = commonprefix(strings)
    index = len(prefix)
    l=min(len(s) for s in strings)
    ticks=[0 for x in range(index+1)] # `+1` allows for the match to be between prefix and the next letter
    # Find the last shared word barrier
    split=0
    barrier_source = [BARRIER.finditer(string) for string in strings]
    while barrier_source: # not exactly idiomatic, but it prevents us from entering if there are no strings
        try:
            barriers = [next(b).start() for b in barrier_source] # where all the barriers are
            while len(set(barriers)) != 1:
                i = index_of_lowest_element(barriers)
                if barriers[i] > index: raise StopIteration
                ticks[barriers[i]] += 1
                barriers[i] = next(barrier_source[i]).start()
            ticks[split] = len(strings) # allowed to look past the common prefix
            if barriers[0] > index:
                break
            split = barriers[0] # they all agreed. Keep this answer, go to the top and try again
        except StopIteration: # a finditer finished its run
            break
    if False:
        for string in strings:
            print("DEBUG:", string)
        print("DEBUG:", prefix)
        print("DEBUG:", ''.join(chr(ord('0') + t) for t in ticks))
    return prefix[:split]

DEFAULT_COMMON=common_word_barrier

def calc_args(argv):
    args = argparse.ArgumentParser(description='Remove common prefixes between lines of input. Works best on already-sorted input')
    args.add_argument("files", nargs="*") # default = none
    group = args.add_mutually_exclusive_group()
    group.add_argument("--wordwise", "-w", action='store_const', dest='commonStrat', const=common_word_barrier, help="break on on a word barrier (default)")
    group.add_argument("--pathwise", "-p", action='store_const', dest='commonStrat', const=commonpath, help="only break on path separators")
    group.add_argument("--textwise", "-t", action='store_const', dest='commonStrat', const=commonprefix, help="recognize any text as the common prefix")
    group.add_argument("--elision-marker", default=ELISION_MARKER, help="the indicator that a piece has been removed")
    args.set_defaults(commonStrat=DEFAULT_COMMON)
    out = args.parse_args(argv)
    return out.__dict__

def run_on_files(files=None, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER):
    with fileinput(files=files) as stdin:
        run(stdin, commonStrat=commonStrat, elision_marker=elision_marker)

def run(stdin, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER):
    prev=''
    for line in stdin:
        line = line.strip()
        do_line(prev, line, commonStrat=DEFAULT_COMMON, elision_marker=elision_marker)
        prev = line


def do_line(prev, line, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER):
    prefix = commonStrat([prev, line])
    index = len(prefix) # with commonpath, this is stopped BEFORE the common slash
    paranoia = commonprefix([line[index:], prev[index:]])

    if index >= len(elision_marker):
        prefix = ' '*(index-len(elision_marker)) + elision_marker
    else:
        prefix = ' ' * index
    print(prefix + line[index:])


def main():
    args = calc_args(sys.argv[1:])
    run_on_files(**args)

if __name__ == '__main__':
    try:
        main()
    except (BrokenPipeError, IOError, KeyboardInterrupt):
        exit(55)
