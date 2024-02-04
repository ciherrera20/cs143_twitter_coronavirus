#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import sys
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
items = items[:10]  # Get only the top 10 keyss
items = list(zip(*items))  # Transpose list
xlabel = os.path.splitext(args.input_path)[1]
if xlabel != '':
    xlabel = xlabel[1:]
plt.bar(range(len(items[0])), items[1])  # With matplotlib 2.1.1, giving strings as the first argument causes the graph to be sorted alphabetically. We get around this by first passing in numbers and then labelling the x ticks with strings
plt.title(args.key)
plt.xlabel(xlabel)
plt.xticks(range(len(items[0])), items[0])
plt.savefig(sys.stdout.buffer)
plt.close()
