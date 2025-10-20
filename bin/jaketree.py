#!/usr/bin/env python3

from fileinput import input as fileinput
from collections import Counter
from os.path import commonpath, commonprefix
import argparse
import re
import sys # for argv and stdout

# A regex to match word barriers - the zero-width string where we want to cut words.
# Currently, that's at "The| end| of| words| and| also| within| Snake|Case|Words|"
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
DITTO_MARKER='"'
DEBUG=False

def index_of_lowest_element(items):
    lowest = min(items)
    return items.index(lowest)


def debug_print_string_with_barriers_and_gaps(string, barriers, gaps):
    """
    A way to visualize where a match is/isn't.
    Barriers are indexes where matches ARE.
    Gaps are where they COULD be.
    Barriers not listed in the gap set are ignored
    """
    prev = 0
    for i in sorted(set(gaps)):
        sigil = '|' if i in barriers else ' '
        print(string[prev:i], sigil, sep='', end='')
        prev = i
    # Naturally accomplish both:
    # * any leftover parts of the string
    # * the trailing newline
    print(string[prev:])


# Find a good word barrier somewhere within the common text of the given strings that counts
# as a word barrier in all the strings. This may be the common prefix, but could be shorter.
# Consider fooBar and fooBaz - the common string prefix is `fooB`, but the common word prefix is `foo`
# Likewise, food and fool have no common word prefix.
def common_word_barrier(strings, debug=None):
    if debug is None: # default from global
        debug = DEBUG
    prefix = commonprefix(strings)
    if debug:
        print("DEBUG:", f'{prefix=} {strings=}')
    tooFar = len(prefix)
    barrierVotes = Counter()
    for s in strings:
        for match in BARRIER.finditer(s):
            start = match.start()
            if start > tooFar:
                break
            barrierVotes[start] += 1
    if debug:
        for s in strings:
            debug_print_string_with_barriers_and_gaps(
                s,
                barriers = set(match.start() for match in BARRIER.finditer(s)),
                gaps = barrierVotes.keys())
    for candidate in reversed(sorted(barrierVotes.keys())):
        if barrierVotes[candidate] == len(strings):
            return prefix[:candidate]
    # No candidate had enough votes. No common prefix
    return ""

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
    args.add_argument("--ditto-marker", default=DITTO_MARKER, help=f"the indicator that the whole line is duplicated ({DITTO_MARKER})")
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

def run_on_files(files=None, **kwargs):
    with fileinput(files=files) as stdin:
        run(stdin, **kwargs)

def run(stdin, **kwargs):
    prev=''
    for line in stdin:
        line = line.rstrip("\r\n") # strip trailing newlines. This permits print to add its own end=..
        do_line(prev, line, **kwargs)
        prev = line


def do_line(prev, line,
            commonStrat=DEFAULT_COMMON,
            elision_marker=ELISION_MARKER,
            ditto_marker=DITTO_MARKER,
            output=print,
            debug=None):
    if debug is None:
        debug = DEBUG # currently unused, but respecting the pattern
    prefix = commonStrat([prev, line])
    index = len(prefix) # with commonpath, this is stopped BEFORE the common slash
    paranoia = commonprefix([line[index:], prev[index:]])

    # Optionally: if the texts are the same, print a ditto marker instead
    if len(prev) == index == len(line):
        elision_marker=ditto_marker

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
