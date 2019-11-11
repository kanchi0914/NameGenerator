import numpy as np
from . import sequences_maker

def sample(preds, temperature=0.4):
    preds = np.asarray(preds).astype('float64')
    if temperature == 0:
        # Avoiding a division by 0 error
        return np.argmax(preds)
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def generate_name(model, start, *, chars, temperature=0.4):
    maxlength = model.layers[3].input.shape[1]
    seqlen = int(model.layers[0].input.shape[1])
    result = start

    sequence_input = np.zeros(shape=(1, seqlen, len(chars)))
    for i, char in enumerate(start):
        sequence_input[0, i, chars.index(char)] = 1.

    length_input = np.zeros(shape=(1, maxlength))
    length_input[0, len(result) - 1] = 1.

    prediction = model.predict(x=[sequence_input, length_input])[0]
    char_index = sample(prediction, temperature)
    while char_index < len(chars) - 1 and len(result) < maxlength:
        result += chars[char_index]

        sequence_input = np.zeros(shape=(1, seqlen, len(chars)))
        for i, char in enumerate(result[(-seqlen):]):
            sequence_input[0, i, chars.index(char)] = 1.

        length_input[0, len(result) - 2] = 0.
        length_input[0, len(result) - 1] = 1.

        prediction = model.predict(x=[sequence_input, length_input])[0]
        char_index = sample(prediction, temperature)

    return result.title()

def generate_random_name(model, *, chars, dictchars, temperature=0.4):
    start = sequences_maker.generate_start_seq(dictchars)
    return generate_name(model, start, chars=chars, temperature=temperature)
