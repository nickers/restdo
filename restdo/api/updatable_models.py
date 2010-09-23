# -*- coding: utf-8 -*-
#from django.views.decorators.http import etag
from django.http import QueryDict, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from piston.handler import BaseHandler, etag
from django.forms import ValidationError
from piston.utils import rc

import simplejson as json
import hashlib
import urllib

## self explanatory ;)
def md5sum(obj):
	dict = {}
	for o in obj.__dict__:
		if o[0]!='_':
			dict[o] = obj.__dict__[o]
	return hashlib.md5(unicode(dict).encode("iso-8859-1","ignore")).hexdigest()

def md5func(model):
	def md5tag_book(request, **kwargs):
		try:
			print 'Last generated etag: ', md5sum(model.objects.get(**kwargs))
			return md5sum(model.objects.get(**kwargs))
		except model.DoesNotExist:
			return None
		except:
			print "Should I do some debugging? Btw. yous md5tag function sucks!"
			return None
	return md5tag_book


class UpdatableModels(BaseHandler):
	allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
	url_name = None


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

		return HttpResponseRedirect(reverse(self.url_name, kwargs={'id':inst.id}))


	def update(self, request, **kwargs):
		ret = rc.ALL_OK

		try:
			obj = self.model.objects.get(**kwargs)

			# require etag for non-empty objects
			if not (obj.isEmpty() or ("HTTP_IF_MATCH" in request.META)):
				return HttpResponse(status=412) # precondition failed
		except self.model.DoesNotExist:
			obj = self.model()
			obj.id = kwargs['id']
			ret = rc.CREATED

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
			
		return ret

	def delete(self, request, **kwargs):
		try:
			obj = self.model.objects.get(**kwargs)
			# require etag for non-empty objects
			if not (obj.isEmpty() or ("HTTP_IF_MATCH" in request.META)):
				return HttpResponse(status=412) # precondition failed
		except self.model.DoesNotExist:
			None
		return super(UpdatableModels, self).delete(request, **kwargs)

