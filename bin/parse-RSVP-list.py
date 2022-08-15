#! /usr/bin/env python3

import csv
import fileinput
from pprint import pprint
from collections import defaultdict, Counter

j = csv.reader(fileinput.input())
a= list(j)
head=a[0]
data=a[1:]
#  ('Not Sent', 120), ('No Response', 88), ('Attending', 29),
categorize = {"No Response", "Not Sent", 'No Response', 'Attending', "Regret"}
out=Counter()
cats = defaultdict(set)

ignore={"First Name", "Last Name", "Party", "Not Sent", "No Response", "My Notes"}

resp = defaultdict(set)
for d in data:
    for i in range(len(d)):
        f = d[i]
        out[f]+=1
        if f in ignore or head[i] in ignore:
            pass
        elif f in categorize:
            cats[head[i] + ": "+ f].add(d[0] + " " + d[1])
        elif f:
            resp[head[i]].add(f + " - " + d[0] + " " + d[1])

for head in resp:
    print()
    print("==", head, "==", end="")
    print("".join("\n\t * " + r for r in resp[head]))

for c in cats:
    print()
    print("==", c, "==", end="")
    print("".join("\n\t" + p for p in cats[c]))

