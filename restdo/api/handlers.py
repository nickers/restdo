# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from piston.utils import rc
from books.models import Book
from books_lends.models import BookLend
from readers.models import Reader
from api.updatable_models import UpdatableModels, md5func
import re
from datetime import datetime

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

#### #### #### #### ####
class BooksQueueHandler(BaseHandler):
	allowed_methods = ('GET', 'DELETE')# 'POST', 'PUT', 'DELETE')
	model = BookLend
	##exclude = (re.compile('^private_'), 'book')

	def getBooksQuery(self, book_id):
		query = BookLend.objects.filter(book__id=book_id)
		query = query.filter(**BookLend.notEmptyFilter())
		query = query.filter(return_time__exact=None) # not given back only
		query = query.order_by('request_time')
		return query

	def updateQueue(self, book_id):
		query = self.getBooksQuery(book_id)
		item = query[0]
		doUpdate = True
		for entry in query:
			if entry.lend_time!=None:
				doUpdate = False
		if doUpdate:
			item.lend_time = datetime.now()
			item.save()

	def read(self, request, book_id, **kwargs):
		print kwargs
		try:
			book = Book.objects.get(pk=book_id)
			del book
		except Book.DoesNotExist:
			return rc.NOT_HERE
		query = self.getBooksQuery(book_id)
		return query

	@etag(md5func(BookLend))
	def delete(self, request, book_id, **kwargs):
		book_handler = BookLendHandler()
		r = book_handler.delete(request, id=kwargs['id'])
		self.updateQueue(book_id)
		return r
		#return BaseHandler.delete(book_handler, request, id=kwargs['id'])