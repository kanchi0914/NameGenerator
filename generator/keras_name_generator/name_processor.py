def process_names(names, *, unwanted=['(', ')', '-', '.', '/']):
    names = [name.lower() for name in names]
    print("Total names:", len(names))
    chars = sorted(list(set(''.join(names))))

    def has_unwanted(word):
        for char in word:
            if char in unwanted:
                return True
        return False

    # names = [name for name in names if not has_unwanted(name)]
    # print("Amount of names after removing those with unwanted characters\n:", len(names))
    chars = [char for char in chars if char not in unwanted]
    print("Using the following characters:\n", chars)

    maxes = [len(name) for name in names]
    maxlen = max(maxes)

    # for i, name in enumerate(names):
    #     print(name)
    #     if (len(name) < 2):
    #         print(i)
    #         print(name)


    minlen = min([len(name) for name in names])
    print("Longest name is", maxlen, "characters long")
    print("Shortest name is", minlen, "characters long")

    # enchar indicates the end of the word
    # here it goes through unlikely-to-be-used characters to find one it can use
    endchars = '!£$%^&*()-_=+/?.>,<;:@[{}]#~'
    endchar = [ch for ch in endchars if ch not in chars][0]

    # ensures the character isn't already used & present in the training data
    assert (endchar not in chars)
    chars += endchar

    return names, chars