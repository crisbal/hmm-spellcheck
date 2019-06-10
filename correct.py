import dill
import pybktree
import editdistance
from SpellChecker import SpellChecker
from probabilistic_distance import probabilistic_distance
from collections import defaultdict

print("Loading model...")
words = dill.load(open('model_paisa.dill', 'rb'))

print("Building model...")
for word in words.values():
  successors = word.keys()
  occurrences = word.values()

  prob_factor = 1/sum(occurrences)
  for successor in successors:
    word[successor] *= prob_factor

words_inverse = defaultdict(lambda: defaultdict(float))
"""
print("Building inverse model...")
# build inverse lookup

for predecessor in words.keys():
  for successor in words[predecessor].keys():
    words_inverse[successor][predecessor] += 1

for successor in words_inverse.values():
  predecessors = successor.keys()
  occurrences = successor.values()

  prob_factor = 1/sum(occurrences)
  for pred in predecessors:
    successor[pred] *= prob_factor
# sort inverse lookup
for successor in words_inverse.keys():
  pred_and_probs = words_inverse[successor].items()
  pred_and_probs = sorted(pred_and_probs, key=lambda x: x[1], reverse=True)
  words_inverse[successor] = dict()
  for (pred, probability) in pred_and_probs:
    words_inverse[successor][pred] = probability
"""
print("Building BKTree...")
tree = pybktree.BKTree(editdistance.eval)
[tree.add(word) for word in words.keys()]

print("Ready.")
from Viterbi import Viterbi
viterbi = Viterbi(words, words_inverse, tree)
