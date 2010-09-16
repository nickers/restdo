# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from piston.utils import rc
from books.models import Book

def md5tag(request, param):
	print "Param: ", param
	print "DONE"
	return "sum-md5-test"
	

class BookHandler(BaseHandler):
	allowed_methods = ('GET',)
	model = Book
	
	@etag(md5tag)
	def read(self, request, param):
		resp = rc.ALL_OK
		print 'here'
		return "OKall!"