from collections import defaultdict
from itertools import repeat
from itertools import islice
import subprocess
import string
import re
import os
import config

from nltk import sent_tokenize
import random
if __name__ == "__main__":
  for FILE in os.listdir(config.MODEL):
    if not FILE.endswith('.txt'): continue
    with open(f"{config.MODEL}/{FILE}") as data_file:
      for line in data_file:
        if line.startswith("<text") or line.startswith("</text") or line.startswith("#"): continue
        if random.random() > 0.8:
          sentences = sent_tokenize(line)
          sentence = sentences[0]
          if len(sentence) > 30:
            print(sentence)
