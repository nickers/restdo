# -*- coding: utf-8 -*-
from django.db import models
from books.models import Book
from readers.models import Reader

class BookLend(models.Model):
	book = models.ForeignKey('books.Book')
	reader = models.ForeignKey('readers.Reader')
	request_time = models.DateTimeField('lend request date', auto_now_add=True)
	lend_time = models.DateTimeField('lend date', null=True)
	return_time = models.DateTimeField('returns date', null=True)