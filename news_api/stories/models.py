from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    CategoryTypes = (('pol', 'Politics'),
                     ('art', 'Art'),
                     ('tech', 'Technology'),
                     ('trivia', 'Trivial'))

    RegionTypes = (('uk', 'United Kingdom'),
                   ('eu', 'European'),
                   ('w', 'World'))

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6, choices=CategoryTypes)
    region = models.CharField(max_length=2, choices=RegionTypes)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    publication_date = models.DateTimeField('Publication Date')
    details = models.TextField(max_length=512)
