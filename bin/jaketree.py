#!/usr/bin/env python3

from fileinput import input as fileinput
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv and stdout

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


def flushing_print(*args, **kwargs):
    """print(), but with flush defaulting to true"""
    return print(*args, flush=True, **kwargs)

def calc_args(argv):
    args = argparse.ArgumentParser(description='Remove common prefixes between lines of input. Works best on already-sorted input')
    args.add_argument("files", nargs="*") # default = none
    # I *want* this to be a add_mutually_exclusive_group, but those don't get group titles, and
    # it's annoying that you can't override prior flags with later ones (instead, you get an error)
    group = args.add_argument_group("word-splitting strategies")
    group.add_argument("--wordwise", "-w", action='store_const', dest='commonStrat', const=common_word_barrier, help="break on on a word barrier (default)")
    group.add_argument("--pathwise", "-p", action='store_const', dest='commonStrat', const=commonpath, help="only break on path separators")
    group.add_argument("--textwise", "-t", action='store_const', dest='commonStrat', const=commonprefix, help="recognize any text as the common prefix")
    args.add_argument("--elision-marker", default=ELISION_MARKER, help=f"the indicator that a piece has been removed ({ELISION_MARKER})")
    args.add_argument("--flush", "-f", action='store_const', dest="output", const=flushing_print, help="flush each line as it's printed (turns on automatically if stdout isn't a terminal)")
    args.add_argument("--buffered", action='store_const', dest="output", const=print, help="use traditional buffered output (used for default terminal output)")
    args.set_defaults(commonStrat=DEFAULT_COMMON, output=print)
    if not sys.stdout.isatty():
        args.set_defaults(output=flushing_print)

    out = args.parse_args(argv)
    print(vars(out))
    return vars(out)

def run_on_files(files=None, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER, output=print):
    with fileinput(files=files) as stdin:
        run(stdin, commonStrat=commonStrat, elision_marker=elision_marker, output=output)

def run(stdin, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER, output=print):
    prev=''
    for line in stdin:
        line = line.strip()
        do_line(prev, line, commonStrat=commonStrat, elision_marker=elision_marker, output=output)
        prev = line


def do_line(prev, line, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER, output=print):
    prefix = commonStrat([prev, line])
    index = len(prefix) # with commonpath, this is stopped BEFORE the common slash
    paranoia = commonprefix([line[index:], prev[index:]])

    if index >= len(elision_marker):
        prefix = ' '*(index-len(elision_marker)) + elision_marker
    else:
        prefix = ' ' * index
    output(prefix + line[index:])


def main():
    args = calc_args(sys.argv[1:])
    run_on_files(**args)

if __name__ == '__main__':
    try:
        main()
        # TODO: how do other progams get automatic less pagination to the terminal? Can we do that here, too?
        # ..is https://pypi.org/project/autopage/ viable?
    except (BrokenPipeError, IOError, KeyboardInterrupt):
        exit(55)
