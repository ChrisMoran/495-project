from django.db import models

# Create your models here.

class Rank(models.Model):
    domain = models.CharField(max_length=256) # i don't think domains get this long
    rank = models.BigIntegerField() # django has no bigint, this should be okay for now

class Vote(models.Model):
    query = models.CharField(max_length=1024) # should fit in less than 1kb
    link = models.CharField(max_length=1024)
    vote = models.BooleanField() # true for good, false for bad
