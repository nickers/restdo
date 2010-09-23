# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from books.models import Book
from api.updatable_models import UpdatableModels, md5func
#from decorators import e

	

class BookHandler(UpdatableModels):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	model = Book
	url_name = 'books_api'
	
	@etag(md5func(Book))
	def read(self, request, *args, **kwargs):
		return super(BookHandler, self).read(request, *args, **kwargs)

	@etag(md5func(Book))
	def update(self, request, *args, **kwargs):
		return super(BookHandler, self).update(request, **kwargs)

	@etag(md5func(Book))
	def delete(self, request, *args, **kwargs):
		return super(BookHandler, self).delete(request, **kwargs)
