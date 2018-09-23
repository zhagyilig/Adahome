from django.db import models

# Create your models here.

class Person(models.Model):
    username = models.CharField(max_length=32, null=True)
