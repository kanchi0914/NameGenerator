import numpy as np

def generate_start_seq(dictchars):
    res = ""  # The starting sequence will be stored here
    p = sum([n for n in dictchars[0].values()])  # total amount of letter occurences
    r = np.random.randint(0, p)  # random number used to pick the next character
    tot = 0
    for key, item in dictchars[0].items():
        if r >= tot and r < tot + item:
            res += key
            break
        else:
            tot += item

    for i in range(1, len(dictchars)):
        ch = res[-1]
        if dictchars[i].get(ch, 0) == 0:
            l = list(dictchars[i].keys())
            ch = l[np.random.randint(0, len(l))]
        p = sum([n for n in dictchars[i][ch].values()])
        r = np.random.randint(0, p)
        tot = 0
        for key, item in dictchars[i][ch].items():
            if r >= tot and r < tot + item:
                res += key
                break
            else:
                tot += item
    return res


def make_sequences(names, seqlen, chars):
    sequences, lengths, nextchars = [], [], []  # To have the model learn a more macro understanding,
    # it also takes the word's length so far as input
    for name in names:
        if len(name) <= seqlen:
            sequences.append(name + chars[-1] * (seqlen - len(name)))
            nextchars.append(chars[-1])
            lengths.append(len(name))
        else:
            for i in range(0, len(name) - seqlen + 1):
                sequences.append(name[i:i + seqlen])
                if i + seqlen < len(name):
                    nextchars.append(name[i + seqlen])
                else:
                    nextchars.append(chars[-1])
                lengths.append(i + seqlen)

    print(len(sequences), "sequences of length", seqlen, "made")

    return sequences, lengths, nextchars