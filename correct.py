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
from learn import tokenize_sentence, generalize_tokens
import readline

def rebuild(tokens, correct_tokens):
  rebuilt_tokens = correct_tokens.copy()
  for i, corr_token in enumerate(correct_tokens):
    if corr_token == "PERSON_NAME":
      rebuilt_tokens[i] = tokens[i]
  return rebuilt_tokens

def correct(text):
  sentences = sent_tokenize(text)
  for sentence in sentences:
    print(" ".join(correct_sentence(sentence)))

def correct_sentence(sentence):
  tokens = tokenize_sentence(sentence)
  generalized_tokens = generalize_tokens(tokens)
  corrected_tokens = viterbi.run(generalized_tokens)
  rebuilt_tokens = rebuild(tokens, corrected_tokens)
  return rebuilt_tokens

if __name__ == "__main__":
  while True:
    text = input(">>> ")
    correct(text)
