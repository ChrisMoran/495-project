from django.db import models

# Create your models here.

class Rank(models.Model):
    domain = models.CharField(max_length=256) # i don't think domains get this long
    rank = models.BigIntegerField() # django has no bigint, this should be okay for now

class Vote(models.Model):
    query = models.CharField(max_length=1024) # should fit in less than 1kb
    link = models.CharField(max_length=1024)
    vote = models.BooleanField() # true for good, false for bad

class Search(models.Model):
    query = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now=True)

class Click(models.Model):
    url = models.CharField(max_length=1024)
    search = models.CharField(max_length=1024)
    rank = models.IntegerField()

class Results(models.Model):
    query = models.ForeignKey(Search)
    url = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    description = models.TextField()
