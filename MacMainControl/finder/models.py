from django.db import models

# Create your models here.
from django.db import models


class FinderScript(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

