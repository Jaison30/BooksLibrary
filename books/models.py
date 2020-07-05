# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    book_count = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to='books/',null=True, blank=True)

    def __str__(self):
        return self.name


class BorrowedBook(models.Model):
 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateTimeField('Date', null=True, blank=True)

    def __str__(self):
        return self.user.username