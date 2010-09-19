# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from piston.utils import rc
from books.models import Book
import hashlib
import cgi

def md5tag(request, book_slug):
	try:
		obj = Book.objects.get(slug=book_slug)
		return hashlib.md5(unicode(obj).encode("iso-8859-1","ignore")).hexdigest()
	except Book.DoesNotExist:
		return None
	
# Books

def not_found(id=None):
	ret = rc.ALL_OK
	ret.status_code = 404
	if id==None:
		ret.content = "404 - NOT FOUND"
	else:
		ret.content = "404 - NOT FOUND object %s"%(id,)
	return ret
	

class BookHandler(BaseHandler):
	allowed_methods = ('GET',)#, 'POST', 'PUT', 'DELETE')
	model = Book
	
	@etag(md5tag)
	def read(self, request, book_slug):
		try:
			return Book.objects.get(slug=book_slug)
		except Book.DoesNotExist:
			return not_found(book_slug)
	
	def update(self, request, book_slug):
		return Book.objects.get(slug=book_slug)