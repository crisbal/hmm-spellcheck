from correct import tokenize_sentence, viterbi
from collections import defaultdict
FILE = "data/test_it.txt"

total_lines = 0
ok_lines = 0
with open(FILE, "r") as test_file:
  for correct_line in test_file:
    total_lines += 1
    correct_tokens = tokenize_sentence(correct_line)
    correct_line = " ".join(correct_tokens)

    wrong_line = next(test_file)
    wrong_tokens = tokenize_sentence(wrong_line)
    corrected_tokens = viterbi.run(wrong_tokens)
    corrected_line = " ".join(corrected_tokens)
    if corrected_line == correct_line:
      print("OK", correct_line)
      ok_lines += 1
    else:
      print(correct_line,"-", corrected_line)

print(total_lines)
print(ok_lines)
print(ok_lines/total_lines)
