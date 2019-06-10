import string
import dill
from collections import defaultdict
from multiprocessing import Pool, Manager
import subprocess
from itertools import repeat
from itertools import islice
import re

from nltk import sent_tokenize, wordpunct_tokenize
import numpy as np
import tqdm

pattern = re.compile(r'\W+')
def clean_token(token):
    token = pattern.sub('', token).strip()
    return token if len(token) else None

notable = ['?', 'o', 'è', 'l', 'd', "'", 'n', 'x', 'v', 't', '!', 'b', 'm', 'e', 'g', 'c', '-', 'a', 'i', 's', '"']

words = defaultdict(int)
def parse(line):
    if line.startswith("<text") or line.startswith("</text") or line.startswith("#"): return
    sentences = sent_tokenize(line)
    for sentence in sentences:
        tokens = wordpunct_tokenize(sentence)
        #tokens = filter(lambda t: t not in [',', ':'], tokens)
        tokens = filter(lambda t: t not in string.punctuation, tokens)
        tokens = map(str.lower, tokens)
        tokens = map(clean_token, tokens)
        tokens = filter(None, tokens)
        tokens = list(tokens)
        tokens.append("END_SENTENCE")
        for i, token in enumerate(tokens):
            if i != 0:
                if (prev_token, token) not in words:
                    words[(prev_token, token)] = 0
                words[(prev_token, token)] += 1
            prev_token = token

FILE = 'data/paisa.txt'
N = 900_000
with open(FILE) as data_file:
    n_lines = min(N, int(subprocess.check_output(f'wc -l "{FILE}"', shell=True).split()[0]))
    for line in tqdm.tqdm(islice(data_file, n_lines), total=n_lines):
        parse(line)

words_split = defaultdict(lambda: defaultdict(int))
for (prev_token, token), value in words.items():
    words_split[prev_token][token] = value
words = words_split

dill.dump(words, open('model_paisa.dill', 'wb'))
