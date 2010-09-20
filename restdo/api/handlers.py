# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from piston.handler import BaseHandler, etag
from piston.utils import rc
from books.models import Book
from api.updatable_models import UpdatableModels
import simplejson as json
import hashlib

## self explanatory ;)
def md5sum(obj):
		return hashlib.md5(unicode(obj).encode("iso-8859-1","ignore"))\
		.hexdigest()

def md5func(model):
	def md5tag_book(request, **kwargs):
		try:
			return md5sum(model.objects.get(**kwargs))
		except model.DoesNotExist:
			return None
		except:
			print "Should I do some debugging? Btw. yous md5tag function sucks!"
			print " -> failed for: ", model, slug
			return None
	return
	

class BookHandler(UpdatableModels):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	model = Book
	
	@etag(md5func(Book))
	def read(self, request, *args, **kwargs):
		return super(BookHandler, self).read(request, *args, **kwargs)
