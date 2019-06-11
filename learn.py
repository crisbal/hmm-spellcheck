from collections import defaultdict
from itertools import repeat
from itertools import islice
import subprocess
import string
import re
import os

from nltk import sent_tokenize, wordpunct_tokenize
import dill
import numpy as np
import tqdm

import config

pattern = re.compile(r'[\W_]+')
punct = set(string.punctuation)
def clean_token(token):
  if token in punct: return None
  token = pattern.sub('', token).strip()
  return token or None

names = set([line.strip() for line in open("data/names.txt")])
def replace_names(token):
  if token in names:
    return "PERSON_NAME"
  else:
    return token

def tokenize_sentence(sentence, end_sentence=False):
  sentence = sentence.lower()
  tokens = wordpunct_tokenize(sentence)
  tokens = map(clean_token, tokens)
  tokens = filter(None, tokens)
  tokens = filter(lambda x: all(not i.isdigit() for i in x), tokens)
  tokens = list(tokens)
  if end_sentence:
    tokens.append("END_SENTENCE")
  return tokens

def generalize_tokens(tokens):
  tokens = list(map(replace_names, tokens))
  return tokens

words = defaultdict(int)
def parse(line):
    if line.startswith("<text") or line.startswith("</text") or line.startswith("#"): return
    sentences = sent_tokenize(line)
    for sentence in sentences:
        tokens = tokenize_sentence(sentence, end_sentence=True)
        tokens = generalize_tokens(tokens)
        for i, token in enumerate(tokens):
          if i == 0:
            words[("START_SENTENCE", token)] += 1
          else:
            words[(prev_token, token)] += 1
          prev_token = token

"""FILE = 'data/paisa.txt'
N = 100_000
with open(FILE) as data_file:
  n_lines = min(N, int(subprocess.check_output(f'wc -l "{FILE}"', shell=True).split()[0]))
  for line in tqdm.tqdm(islice(data_file, n_lines), total=n_lines):
    parse(line)
"""

if __name__ == "__main__":
  MAX_LINES = 900_000
  for FILE in os.listdir(config.MODEL):
    if not FILE.endswith('.txt'): continue
    with open(f"{config.MODEL}/{FILE}") as data_file:
      n_lines = min(MAX_LINES, int(subprocess.check_output(f'wc -l "{config.MODEL}/{FILE}"', shell=True).split()[0]))
      for line in tqdm.tqdm(islice(data_file, n_lines), total=n_lines):
        parse(line)

  words_split = defaultdict(lambda: defaultdict(int))
  for (prev_token, token), value in words.items():
      words_split[prev_token][token] = value
  words = words_split

  dill.dump(words, open(f"{config.MODEL}/words.dill", 'wb'))
