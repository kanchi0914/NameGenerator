from keras.models import Model, load_model, save_model
import keras
from .keras_name_generator import dictchars_maker, model_setter, name_generator,\
    name_processor, onehot_vec_maker, sequences_maker, csv_loader
from django.conf import settings
import os
import logging

class Names():
    def __init__(self):
        self.load()

    def load(self):
        base2 = settings.BASE_DIR + r"\generator\keras_name_generator" + "\\"

        self.model = load_model(base2 + r"models\model.h5")
        self.model.load_weights(base2 + r"weights\weights7.h5")

        self.datas = csv_loader.load_csv(base2 + r"csv\en_jp_names.csv")
        self.names = [data[1] for data in self.datas]
        self.names, self.chars = name_processor.process_names(self.names)

        seqlen = 4
        self.dictchars = dictchars_maker.get_dictchars(self.names, seqlen)
        # with keras.backend.get_session().graph.as_default():

    def get_name(self):
        list = self.get_names()
        text = ""
        for t in list:
            text += t + "\n"
        return text

    def get_names(self):
        list = []
        for i in range(10):
            list.append(name_generator.generate_random_name
                        (self.model, chars=self.chars, dictchars=self.dictchars))
        return list
        # with keras.backend.get_session().as_default():  #追加

