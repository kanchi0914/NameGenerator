from django.shortcuts import render
from django.views import generic
from .models import TestModel
import keras
from django.views.generic import View
from django.http.response import HttpResponse
from django.http.response import JsonResponse

from keras.models import Model, load_model, save_model
from .keras_name_generator import dictchars_maker, model_setter, name_generator,\
    name_processor, onehot_vec_maker, sequences_maker, csv_loader
from django.conf import settings

class Names():
    def __init__(self):
        self.country = ""
        self.load("en")

    def load(self, country):

        self.country = country

        base2 = settings.BASE_DIR + r"namegenerator\static\data" + "\\"

        self.model = load_model(base2 + r"models\model_" + country + ".h5")
        self.model.load_weights(base2 + r"weights\weights_" + country + ".h5")
        self.datas = csv_loader.load_csv(base2 + r"csv" + "\\" + country + "_jp_names.csv")

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


generator = Names()
# generator.get_names()

# Create your views here.
class IndexView(generic.ListView):
    model = TestModel
    template_name = 'sample/index.html'

def generator_template(request):
    return render(request, "generator/index.html")

def exec_ajax(request):
    # names2 = Names()
    country = request.GET.get("param1")
    if generator.country != country:
        keras.backend.clear_session()
        generator.load(country=country)

    names = generator.get_names()
    if request.method == 'GET':
        return JsonResponse(names, safe=False)


