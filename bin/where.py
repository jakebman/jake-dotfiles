#! /bin/env python3

# TODO: potentially use pathlib instead
from os.path import islink, realpath
from sys import argv

def lines_annotate_cwds(lines):
	"""
		For each word-that-is-a-number in the input, if /proc/{that-number}/cwd exists, append "some meaningful" information about that process's cwd

		Try to be streaming about this
	"""
	for line in lines:
		yield line_annotate_cwds(line)

def line_annotate_cwds(line):
	out = ""
	for word in line.split(" "): # TODO: configurable rejoining
		annotation = False

		if word.isnumeric():
			path = f"/proc/{word}/cwd" # TODO: path-like is allowed, so this might not require string interpolation and could be better
			try:
				if islink(path):
					rpath = realpath(path)
					annotation = f"at {rpath}"
			except PermissionError:
				annotation = "permission denied" # TODO: who might be the owner?

		if out:
			out += " " # TODO: configurable rejoining
		out += word
		if annotation:
			out += f" ({annotation})"

	return out


def main():
	on_cli = argv[1:] # skip the program's name
	if on_cli:
		for arg in on_cli:
			print(line_annotate_cwds(arg))
	else:
		for line in lines_annotate_cwds(all_input()):
			print(line)

# TODO: fileinput tech from jaketree.py
# Currently, we only accept stdin and numbers as params. Taking cat-like params seems like a reasonable add. Not a big deal to be flexible to accpet numbers and files on the cli
def all_input():
    try:
        while True:
            yield input()
    except EOFError:
        return


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
