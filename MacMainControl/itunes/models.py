from django.db import models

# Create your models here.
from django.db import models


class ItunesScript(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def read_script(self, filename):
        file_object = open(filename)
        try:
            file_context = file_object.read()
        finally:
            file_object.close()
        return file_context
