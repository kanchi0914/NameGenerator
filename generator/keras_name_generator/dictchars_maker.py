def get_dictchars(names, seqlen):
    dictchars = [{} for _ in range(seqlen)]

    for name in names:
        if len(name) < seqlen:
            continue
        dictchars[0][name[0]] = dictchars[0].get(name[0], 0) + 1
        for i in range(1, seqlen):
            if dictchars[i].get(name[i - 1], 0) == 0:
                dictchars[i][name[i - 1]] = {name[i]: 1}
            elif dictchars[i][name[i - 1]].get(name[i], 0) == 0:
                dictchars[i][name[i - 1]][name[i]] = 1
            else:
                dictchars[i][name[i - 1]][name[i]] += 1
    return dictchars