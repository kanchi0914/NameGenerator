from . import dictchars_maker, model_setter, name_generator,\
    name_processor, onehot_vec_maker, sequences_maker, csv_loader

def train(model_path, weights_path):
    datas = csv_loader.load_csv("csv/en_jp_names.csv")
    names = [data[1] for data in datas]
    names, chars = name_processor.process_names(names)

    seqlen = 4
    sequences, lengths, nextchars = sequences_maker.make_sequences(names, seqlen, chars)
    dictchars = dictchars_maker.get_dictchars(names, seqlen)


    x, x2, y = onehot_vec_maker.make_onehots(sequences=sequences,
                                             lengths=lengths,
                                             nextchars=nextchars,
                                             chars=chars)

    model = model_setter.make_model(x, x2, chars)


    train_model(model, x=x, x2=x2, y=y, chars=chars, dictchars=dictchars)

    model.save(model_path)
    model.save_weights(weights_path)

    for _ in range(20):
        print(name_generator.generate_random_name
              (model, chars=chars, dictchars=dictchars))


def train_model(model, *, x, x2, y, chars, dictchars, total_epochs=180,
              print_every=60, temperature=0.4, verbose=True):
    for i in range(total_epochs//print_every):
        history = model.fit([x,x2],y,
                            epochs=print_every,
                            batch_size=64,
                            validation_split=0.05,
                            verbose=0)
        if verbose:
            print("\nEpoch",(i+1)*print_every)
            print("First loss:            %1.4f" % (history.history['loss'][0]))
            print("Last loss:             %1.4f" % (history.history['loss'][-1]))
            print("First validation loss: %1.4f" % (history.history['val_loss'][0]))
            print("Last validation loss:  %1.4f" % (history.history['val_loss'][-1]))
            print("\nGenerating random names:")
            for _ in range(10):
                print(name_generator.generate_random_name
                      (model,chars=chars,dictchars=dictchars,temperature=temperature))

    if not verbose:
        print("Model training complete, here are some generated names:")
        for _ in range(50):
            print(name_generator.generate_random_name
                  (model,chars=chars,dictchars=dictchars,temperature=0.4))
