#!/usr/bin/env python3

from fileinput import input
from os.path import commonpath as common # import commonpath here instead, for files, or commonprefix here for text

def deserveElipsis(index, line):
    if index < 3: return False
    if index >= len(line): return False
    if '/' != line[index]: return True
    return False

def main():
    prev=''
    with input() as stdin:
        for line in stdin:
            line = line.strip()
            prefix = common([line, prev])
            index = len(prefix)
            if deserveElipsis(index, line):
                prefix = ' '*(index-3) + '...'
            else:
                prefix = ' ' * index
            print(prefix + line[len(prefix):], flush=True)
            prev = line

if __name__ == '__main__':
    main()
