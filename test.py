from correct import tokenize_sentence, viterbi
from collections import defaultdict
import random

FILE = "data/test_it.txt"

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
           'n','o','p','q','r','s','t','u','v','w','x','y','z',]

def noise_maker(sentence, threshold=0.9):
  noisy_sentence = []
  i = 0

  while i < len(sentence):
    do_error = random.random()
    if do_error < threshold:
      noisy_sentence.append(sentence[i])
    else:
      error_type = random.choice([1,2,3])
      if error_type == 1:
        # inversion
        if i == (len(sentence) - 1):
          continue
        else:
          if sentence[i] != ' ' and sentence[i+1] != ' ':
            print("INVERSION ", (sentence[i], sentence[i+1]))
            noisy_sentence.append(sentence[i+1])
            noisy_sentence.append(sentence[i])
            i += 1
          else:
            i -= 1 # riconsidero la stessa lettera nell'iterazione successiva
      elif error_type == 2:
        #aggiunta

        random_letter = random.choice(letters)
        noisy_sentence.append(random_letter)
        noisy_sentence.append(sentence[i])
        print("AGGIUNTA ", random_letter)
      elif error_type == 3:
        # remove a letter
        print("OMISSION")
        if sentence[i] != ' ':
          pass
        else:
          noisy_sentence.append(sentence[i])
      else:
          noisy_sentence.append(sentence[i])
    i += 1
  return "".join(noisy_sentence)

total_lines = 0
ok_lines = 0
with open(FILE, "r") as test_file:
  for correct_line in test_file:
    total_lines += 1
    correct_tokens = tokenize_sentence(correct_line)
    correct_line = " ".join(correct_tokens)

    noised_sentence = noise_maker(correct_line, 0.9)
    #noised_sentence = "".join(noised_sentence_list)
    #print("\t\t", noised_sentence)
    noised_sentence = tokenize_sentence(noised_sentence)
    #print("\t", noised_sentence)

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
