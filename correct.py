from collections import defaultdict

import dill
import pybktree
import editdistance

import config
from probabilistic_distance import probabilistic_distance

print("Loading model...")
model = dill.load(open(f"{config.MODEL}/model.dill", 'rb'))
words = model['words']
words_inverse = model['words_inverse']
tree = model['tree']

print("Ready.")
from Viterbi import Viterbi
viterbi = Viterbi(words, words_inverse, tree)

import string
from nltk import sent_tokenize, wordpunct_tokenize
from learn import tokenize_sentence
import readline

def correct(text):
  sentences = sent_tokenize(text)
  for sentence in sentences:
    tokens = tokenize_sentence(sentence)
    return " ".join(viterbi.run(tokens))

def correct_sentence(sentence):
  tokens = tokenize_sentence(sentence)
  return viterbi.run(tokens)

if __name__ == "__main__":
  while True:
    text = input(">>> ")
    print(correct(text))
