#!/usr/bin/env python3

from fileinput import input as fileinput
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv and stdout

# A regex to match word barriers - the zero-width string where we want to cut words.
# Currently, that's at |The |start |of |words |and |also |within |Snake|Case|Words
# Broken down:
# (?<=\w)(?=\W|$)
#   A word barrier. Essentially r'\b', but only at the end of words:
#   a \word character followed by a non-\Word character or eol
# (<=[a-z])(?=[A-Z])
#   The SnakeCaseWordBarriers. A lowercase letter followed by an upercase one.
#   Unicode support available if I grab `regex` from pypi. Would become:
#   `(<=\p{Lowercase_Letter})(?=\p{Uppercase_Letter}|\p{Titlecase_Letter})'`
#   https://stackoverflow.com/questions/68428413/how-do-i-match-all-unicode-lowercase-characters-in-python-with-a-regular-express
BARRIER=re.compile(r'(?<=\w)(?=\W|$)|(?<=[a-z])(?=[A-Z]|$)')
ELISION_MARKER='…'
DEBUG=False

def index_of_lowest_element(items):
    lowest = min(items)
    return items.index(lowest)


def debug_print_strings_with_barriers(strings, barriers, index=None, debug=None):
    if debug is None: # default from global
        debug = DEBUG
    if not debug:
        return
    if index is None: # client doesn't care which index. Any will do.
        index = barriers[0]

    for i in range(len(strings)):
        print("DEBUG:", f'{strings[i][:barriers[i]]}|{strings[i][barriers[i]:]}', ('*' if i == index else ''))

def common_word_barrier(strings, debug=None):
    if debug is None: # default from global
        debug = DEBUG
    prefix = commonprefix(strings)
    if debug:
        print("DEBUG:", f'{prefix=}')
    index = len(prefix)
    l=min(len(s) for s in strings)
    # Find the last shared word barrier
    split=0
    barrier_source = [BARRIER.finditer(string) for string in strings]
    while barrier_source: # not exactly idiomatic (I'd prefer `if`), but it allows internal breaks from this block
        try:
            barriers = [next(b).start() for b in barrier_source] # where all the barriers are
            while len(set(barriers)) != 1:
                i = index_of_lowest_element(barriers)
                if barriers[i] > index: raise StopIteration
                debug_print_strings_with_barriers(strings, barriers, index=i, debug=debug)
                barriers[i] = next(barrier_source[i]).start()
            else:
                debug_print_strings_with_barriers(strings, barriers, debug=debug)

            if barriers[0] > index:
                break
            split = barriers[0] # they all agreed. Keep this answer, go to the top and try again
        except StopIteration: # a finditer finished its run
            break
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
    args.add_argument("--debug", action='store_const', dest="debug", const=True, help="Enable debug output")
    args.set_defaults(commonStrat=DEFAULT_COMMON, output=print)
    if not sys.stdout.isatty():
        args.set_defaults(output=flushing_print)

    out = args.parse_args(argv)
    global DEBUG
    DEBUG = out.debug
    return vars(out)

def run_on_files(files=None, commonStrat=DEFAULT_COMMON, elision_marker=ELISION_MARKER, output=print, **_ignored_kwargs):
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
