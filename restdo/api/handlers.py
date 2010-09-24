# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from piston.utils import rc
from books.models import Book
from books_lends.models import BookLend
from readers.models import Reader
from api.updatable_models import UpdatableModels, md5func
import re

per_page_items = 5
	
## Book
class BookHandler(UpdatableModels):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	exclude = (re.compile('^private_'),)
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

class BooksListHandler(BookHandler):
	allowed_methods = ('GET')

	def read(self, request, page_number, *args, **kwargs):
		if int(page_number)<0:
			return rc.NOT_HERE
		list = super(BooksListHandler, self).read(request, *args, **kwargs).order_by(self.model._meta.pk.name)
		list = list[int(page_number)*per_page_items:int(page_number)*per_page_items+per_page_items]
		if len(list)==0:
			return rc.NOT_HERE
		return list


## BookLend
class BookLendHandler(UpdatableModels):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	model = BookLend
	exclude = (re.compile('^private_'),)
	url_name = 'lends_api'

	@etag(md5func(BookLend))
	def read(self, request, *args, **kwargs):
		return super(BookLendHandler, self).read(request, *args, **kwargs)

	@etag(md5func(BookLend))
	def update(self, request, *args, **kwargs):
		return super(BookLendHandler, self).update(request, **kwargs)

	@etag(md5func(BookLend))
	def delete(self, request, *args, **kwargs):
		return super(BookLendHandler, self).delete(request, **kwargs)


class BookLendsListHandler(BookLendHandler):
	allowed_methods = ('GET')

	def read(self, request, page_number, *args, **kwargs):
		if int(page_number)<0:
			return rc.NOT_HERE
		list = super(BookLendsListHandler, self).read(request, *args, **kwargs).order_by(self.model._meta.pk.name)
		list = list[int(page_number)*per_page_items:int(page_number)*per_page_items+per_page_items]
		if len(list)==0:
			return rc.NOT_HERE
		return list

## Reader
class ReaderHandler(UpdatableModels):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	model = Reader
	exclude = (re.compile('^private_'),)
	url_name = 'reader_api'

	@etag(md5func(Reader))
	def read(self, request, *args, **kwargs):
		return super(ReaderHandler, self).read(request, *args, **kwargs)

	@etag(md5func(Reader))
	def update(self, request, *args, **kwargs):
		return super(ReaderHandler, self).update(request, **kwargs)

	@etag(md5func(Reader))
	def delete(self, request, *args, **kwargs):
		return super(ReaderHandler, self).delete(request, **kwargs)

class ReadersListHandler(ReaderHandler):
	allowed_methods = ('GET')

	def read(self, request, page_number, *args, **kwargs):
		if int(page_number)<0:
			return rc.NOT_HERE
		list = super(ReadersListHandler, self).read(request, *args, **kwargs).order_by(self.model._meta.pk.name)
		list = list[int(page_number)*per_page_items:int(page_number)*per_page_items+per_page_items]
		if len(list)==0:
			return rc.NOT_HERE
		return list