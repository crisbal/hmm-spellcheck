from correct import tokenize_sentence, viterbi
from collections import defaultdict
import numpy as np

FILE = "data/test_it.txt"

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z',]

def noise_maker(sentence, threshold=0.5):
  noisy_sentence = []
  i = 0
  while i < len(sentence):
    random = np.random.uniform(0,1,1)
    if random < threshold:
      noisy_sentence.append(sentence[i])
    else:
      new_random = np.random.uniform(0,1,1)
      if new_random > 0.67:
        if i == (len(sentence) - 1):
          continue
        else:
          noisy_sentence.append(sentence[i+1])
          noisy_sentence.append(sentence[i])
          i += 1
      elif new_random < 0.33:
        random_letter = np.random.choice(letters, 1)[0]
        #noisy_sentence.append(vocab_to_int[random_letter])
        noisy_sentence.append(sentence[i])
      else:
        pass
    i += 1
  return noisy_sentence

total_lines = 0
ok_lines = 0
with open(FILE, "r") as test_file:
  for correct_line in test_file:
    total_lines += 1
    correct_tokens = tokenize_sentence(correct_line)
    correct_line = " ".join(correct_tokens)

    noised_sentence_list = noise_maker(correct_line, 0.9)
    noised_sentence = "".join(noised_sentence_list)
    noised_sentence = tokenize_sentence(noised_sentence)
    print("\t", noised_sentence)

    wrong_line = next(test_file)
    wrong_tokens = tokenize_sentence(wrong_line)
    #corrected_tokens = viterbi.run(wrong_tokens)
    corrected_tokens = viterbi.run(noised_sentence)
    corrected_line = " ".join(corrected_tokens)
    if corrected_line == correct_line:
      print("OK", correct_line)
      ok_lines += 1
    else:
      print(correct_line,"-", corrected_line)

print(total_lines)
print(ok_lines)
print(ok_lines/total_lines)
