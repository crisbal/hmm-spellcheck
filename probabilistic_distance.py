from functools import lru_cache

OMISSION_RATE = 0.80/100 #%
INSERTION_RATE = 0.67/100 #%
SUBSTITUTION_RATE = 1.65/100 #%
CORRECT_RATE = 1 - OMISSION_RATE - INSERTION_RATE - SUBSTITUTION_RATE #%

@lru_cache(maxsize=None)
def probabilistic_distance(s, t):
    rows = len(s)+1
    cols = len(t)+1
    dist = [[0 for x in range(cols)] for x in range(rows)]
    dist[0][0] = 1
    # source prefixes can be transformed into empty strings
    # by deletions:
    for i in range(1, rows):
        dist[i][0] = OMISSION_RATE ** i
    # target prefixes can be created from an empty source string
    # by inserting the characters
    for i in range(1, cols):
        dist[0][i] = INSERTION_RATE ** i

    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = CORRECT_RATE
            else:
                cost = SUBSTITUTION_RATE
            dist[row][col] = max(
                dist[row-1][col] * OMISSION_RATE,      # deletion
                dist[row][col-1] * INSERTION_RATE,      # insertion
                dist[row-1][col-1] * cost) # substitution
    #print_dist(s, t, dist)
    return dist[-1][-1]

def print_dist(s, t, dist):
    t = '€' + t
    _ = "\t\t"
    for ch in t:
        _ += (f"{ch}\t\t")
    print(_)
    s = '€' + s
    for i, row in enumerate(dist):
        _ = f"{s[i]}\t"
        for col in row:\
            _ += (f"{col*100:.6f}\t")
        print(_)
