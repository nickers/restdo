# -*- coding: utf-8 -*-
from django.views.decorators.http import etag
from django.http import QueryDict, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from piston.handler import BaseHandler, etag
from django.forms import ValidationError
from piston.utils import rc
from books.models import Book

import simplejson as json
import hashlib
import urllib

## self explanatory ;)
def md5sum(obj):
		return hashlib.md5(unicode(obj).encode("iso-8859-1","ignore"))\
		.hexdigest()

def md5func(model):
	def md5tag_book(request, **kwargs):
		try:
			obj = model.objects.get(**kwargs)
			if obj.isEmpty():
				return None
			return md5sum(obj)
		except model.DoesNotExist:
			return None
		except:
			print "Should I do some debugging? Btw. yous md5tag function sucks!"
			print " -> failed for: ", model, slug
			return None
	return
	

class UpdatableModels(BaseHandler):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	#model = Book
	
	
	def flatten_dict(self, request):
		"""
		Return dictionary containing model data.
		"""
		raw_data = ""
		if isinstance(request, QueryDict):
			raw_data = urllib.unquote_plus(request.urlencode()).rstrip("=")
		else:
			raw_data = request.raw_post_data

		return json.loads(unicode(raw_data, 'utf-8'), 'utf-8')
		
	
	#@etag(md5func(Book))
	def read(self, request, *args, **kwargs):
		obj = super(UpdatableModels, self).read(request, *args, **kwargs)
		if hasattr(obj,'isEmpty') and obj.isEmpty():
			return rc.NOT_HERE
		if hasattr(obj,'filter'):
			obj = obj.filter(**self.model.notEmptyFilter())
		return obj

	def create(self, request, *args, **kwargs):
		pkfield = self.model._meta.pk.name
		if pkfield in kwargs and kwargs[pkfield]!='':
			return rc.BAD_REQUEST
		inst = self.model()
		inst.save()

		return HttpResponseRedirect(reverse('books_api',kwargs={'id':inst.id}))
		return rc.ALL_OK
		#return super(UpdatableModels, self).create(request, *args, **kwargs)
		
		# object exists - can't create, must update
		return rc.DUPLICATE_ENTRY
	
	def update(self, request, **kwargs):
		obj = self.model.objects.get(**kwargs)
		json_data = self.flatten_dict(request)

		for prop in json_data:
			try:
				setattr(obj, prop, json_data.get(prop))
			except:
				bad_request = rc.BAD_REQUEST
				msg = {'invalid_key':prop, 'msg':'Invalid key provided.'}
				bad_request.content = json.dumps(msg, encoding='utf-8')
				bad_request['Content-Type'] = 'application/json; charset=utf-8'
				return bad_request
		try:
			obj.save()
		except ValidationError, e:
			bad_request = rc.BAD_REQUEST
			msg = {'msg':e.messages[0]}
			bad_request.content = json.dumps(msg, encoding='utf-8')
			bad_request['Content-Type'] = 'application/json; charset=utf-8'
			return bad_request
			
		return obj
		