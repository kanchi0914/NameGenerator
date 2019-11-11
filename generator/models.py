from django.db import models

# Create your models here.

class TestModel(models.Model):
    name = "test"

    def __str__(self):
        return self.name

