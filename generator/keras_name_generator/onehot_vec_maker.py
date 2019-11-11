import numpy as np

def make_onehots(*, sequences, lengths, nextchars, chars):
    x = np.zeros(shape=(len(sequences), len(sequences[0]), len(chars)), dtype='float32')  # sequences
    x2 = np.zeros(shape=(len(lengths), max(lengths)))  # lengths

    for i, seq in enumerate(sequences):
        for j, char in enumerate(seq):
            x[i, j, chars.index(char)] = 1.

    for i, l in enumerate(lengths):
        x2[i, l - 1] = 1.

    y = np.zeros(shape=(len(nextchars), len(chars)))
    for i, char in enumerate(nextchars):
        y[i, chars.index(char)] = 1.

    return x, x2, y