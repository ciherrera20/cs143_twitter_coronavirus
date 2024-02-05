#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--keys', nargs='+', required=True)
args = parser.parse_args()

# imports
import sys
import os
import json
from datetime import datetime
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# load each of the input paths
dates = []
data = {key: [] for key in args.keys}
pattern = re.compile(r'[^\d]*(\d+)-(\d+)-(\d+)')
for path in args.input_paths:
    match = pattern.match(os.path.split(path)[1])
    dates.append(datetime(year=int('20' + match.group(1)),
                          month=int(match.group(2)),
                          day=int(match.group(3))))
    with open(path) as f:
        tmp = json.load(f)
        for key in args.keys:
            data[key].append(0)
            for n in tmp.get(key, {}).values():
                data[key][-1] += n
                
df = pd.DataFrame(data, index=dates)
df.sort_index(inplace=True)

for key in args.keys:
    plt.plot(df.index, df[key], label=key)
plt.title('Hashtag frequency')
plt.xlabel('Date')
plt.legend()
plt.savefig(sys.stdout.buffer)
plt.close()
