from correct import tokenize_sentence, viterbi
FILE = "data/test_it.txt"

with open(FILE, "r") as test_file:
  for correct_line in test_file:
    correct_tokens = tokenize_sentence(correct_line)
    correct_line = " ".join(correct_tokens)

    wrong_line = next(test_file)
    wrong_tokens = tokenize_sentence(wrong_line)
    corrected_tokens = viterbi.run(wrong_tokens)
    corrected_line = " ".join(corrected_tokens)
    if corrected_line == correct_line:
      print("OK", correct_line)
    else:
      print(correct_line,"-", corrected_line)

