from probabilistic_distance import probabilistic_distance
from collections import defaultdict
from pprint import pprint
from math import log
import numpy as np
from itertools import chain

def bktree_to_set(results):
    return set(map(lambda x: x[1], results))

def get_max_inverse(state, previous_states, model):
  try:
    #max_prob = next(iter(model[state].values()))
    # return the max inverse probability (first since it is ordered dict)
    max_prob = max([model[prev].get(state, 1e-15) for prev in previous_states])
    # la probabilità più alta che tra le possibili parole precedenti si vada nella parola corrente
  except:
    max_prob = 0
  return max_prob

def filter_possible_states(observation, possible_states, previous_states=None, model=None, amount=20):
    if model is None:
      weighted_states = [(state, probabilistic_distance(observation, state)) for state in possible_states]
    else:
      #[model_inverse[state] for state in possible_states]
      weighted_states = [
          (
            state,
            probabilistic_distance(observation, state) * get_max_inverse(state, previous_states, model)
          ) for state in possible_states
      ]
    weighted_states = sorted(weighted_states, key=lambda p: p[1], reverse=True)
    print(weighted_states[:amount])
    possible_states = [state for (state, distance) in weighted_states]
    return possible_states[:amount]

class Viterbi():
    def __init__(self, model,model_inverse, bktree):
        self.model = model
        self.model_inverse = model_inverse
        self.bktree = bktree

    def asd(self, observations):
        if not observations:
            return []

        # all the words with ED <= 2
        starting_states = bktree_to_list(self.bktree.find(observations[0], 1))

        viterbi = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        word_distributions = 1/len(starting_states)
        for starting_state in starting_states:
            # TODO: not uniform probability of starting state
            viterbi[0][starting_state]['_'] = word_distributions * probabilistic_distance(starting_state, observations[0])

        # FRASE BUONGIORNO ALLA MAMMA
        for i, observation in enumerate(observations):
            if i == 0: continue
            previous_states = viterbi[i-1].keys()
            for prev_state in previous_states:
                # tutti gli archi uscenti da "BUONGIORNO"
                possible_states = list(self.model[prev_state].keys())[:3]
                for poss_state in possible_states:
                    viterbi[i][poss_state][prev_state] = max(viterbi[i-1][prev_state].values()) * self.model[prev_state][poss_state] * probabilistic_distance(observation, poss_state)

        for i in range(len(viterbi),0,-1):
            max_value = -1
            max_prev_state = ""
            max_poss_state = ""
            for poss_state in viterbi[i].keys():
                for prev_state in viterbi[i][poss_state].keys():
                    if viterbi[i][poss_state][prev_state] > max_value:
                        max_value = viterbi[i][poss_state][prev_state]
                        max_prev_state = prev_state
                        max_poss_state = poss_state
            print(max_poss_state)

        viterbi = dict(viterbi)
        #self.pprint(viterbi)

    def run2(self, observations):
        T1 = defaultdict(lambda: defaultdict(float))
        T2 = defaultdict(lambda: defaultdict(str))

        starting_states = bktree_to_set(self.bktree.find(observations[0], 3))
        # TODO: improve word distribution
        word_distributions = 1/len(starting_states)
        for state in starting_states:
            T1[0][state] = word_distributions * probabilistic_distance(state, observations[0])
            T2[0][state] = ''

        states = defaultdict(set)
        states[0] = filter_possible_states(observations[0], starting_states)
        print(len(states[0]))
        print(states[0])
        print("\n")
        for j, observation in enumerate(observations):
            if j == 0:
                continue
            print("bktree.find:")
            similar_states = bktree_to_set(self.bktree.find(observation, 3))
            print("possible successors:")
            possible_successor_states = set(chain.from_iterable([ list(self.model[state].keys()) for state in states[j-1] ]))
            states[j] = similar_states | possible_successor_states
            print("filter:")
            states[j] = filter_possible_states(observation, states[j], states[j-1], self.model)
            print("Done")
            #print(len(states[j]))
            #print(states[j])
            print("\n")
            for state in states[j]:
                prev_states = states[j-1]
                probs = [T1[j-1][prev_state] * self.model[prev_state].get(state, 1e-15) * probabilistic_distance(state, observation) for prev_state in prev_states]
                T1[j][state] = max(probs)

                probs2 = [T1[j-1][prev_state] * self.model[prev_state].get(state, 1e-15) for prev_state in prev_states]
                T2[j][state] = prev_states[np.argmax(probs2)]

        # delete last level, not needed
        if len(observations) in states: del states[len(observations)]

        # reconstruct
        T = len(observations) - 1
        X = ['' for i in range(len(observations))]
        X[T] = states[T][np.argmax([T1[T][state] for state in states[T]])]
        for j in range(T, 0, -1):
            X[j-1] = T2[j][X[j]]
        #pprint(T2)
        return X
