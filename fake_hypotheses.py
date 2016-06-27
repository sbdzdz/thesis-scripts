import argparse
import distance
import random
from collections import defaultdict

def add_shuffled(hypo):
    for index, lines in hypo.items(): 
        line = lines[0].strip().split()
        random.shuffle(line)
        hypo[index].append(' '.join(line) + '\n')

def read_unigrams(filename):
    with open(filename, 'r') as f:
        unigrams = [line.split()[0] for line in f]
    return unigrams

def substitute(word):
    global unigrams
    similar = sorted(distance.ifast_comp(word, unigrams))
    return random.choice(similar[1:5][1])

def substitute_words(hypo): 
    for index, lines in hypo.items():
        line = lines[0].strip().split()
        n = len(line)//3 #substitute roughly one third of words
        for position, word in random.sample(list(enumerate(line)), n):
            line[position] = substitute(word)
        hypo[index].append(' '.join(line) + '\n')

def read_hypotheses(filename):
    hypo = defaultdict(list)
    with open(filename, 'r') as f:
        for index, line in enumerate(f):
            hypo[index+1].append(line)
    return hypo

def write_hypotheses(filename, hypo):
    with open(filename + '_hypotheses', 'w') as out:
        for index in sorted(hypo):
            lines = hypo[index]
            for line in lines:
                out.write("{0} {1}".format(index, line))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='path to the input file', type=str)
    args = parser.parse_args()

    unigrams = read_unigrams('unigrams_sorted')
    hypo = read_hypotheses(args.input)
    add_shuffled(hypo)
    substitute_words(hypo)
    write_hypotheses(args.input, hypo)
