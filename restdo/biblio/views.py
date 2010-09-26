# -*- coding: utf-8 -*-

from models import etagBook
from django.http import HttpResponse

def show_book(request, book_id):
	book = etagBook(book_id)
	return HttpResponse(book.getResource().getBody())
