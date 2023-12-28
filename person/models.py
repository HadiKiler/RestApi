from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    number = models.IntegerField(null=True, max_length=12)
    gender = models.SmallIntegerField()
    context = models.TextField()


class Profile(models.Model):
    person = models.ForeignKey(Person, name='person', on_delete=models.CASCADE)
    info = models.TextField()
