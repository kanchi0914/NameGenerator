from keras.layers import LSTM, Dense, Input, concatenate, Reshape, Dropout
from keras.models import Model, load_model, save_model
from . import name_generator
from . import onehot_vec_maker

def make_model(x, x2, chars):
    inp1 = Input(shape=x.shape[1:]) # sequence input
    inp2 = Input(shape=x2.shape[1:]) # length input
    lstm = LSTM(len(chars),activation='relu',dropout=0.3)(inp1)
    lstm2 = LSTM(len(chars),dropout=0.3,go_backwards=True)(inp1)
    concat = concatenate([lstm,lstm2,inp2])
    dense = Dense(len(chars),activation='softmax')(concat)

    model = Model([inp1,inp2],dense)
    model.compile(optimizer='adam',loss='binary_crossentropy')
    return model


