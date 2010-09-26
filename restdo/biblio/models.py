# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from restkit.resource import Resource
import simplejson as json

class etagResource(object):
	def __init__(self, uri, method='get'):
		self.uri = uri
		self.method = method
		self.resource = Resource(self.uri)

	def execute(self, headers=None):
		self.set_result(getattr(self.resource, self.method)(headers=headers))

	def set_result(self, r):
		self.result = r
		self.body_string = self.result.body_string()

	def getEncoding(self):
		return self.result.charset or 'utf8'

	def getBody(self):
		return self.body_string

	def getEtag(self):
		return self.result.headers.get('etag', None)

	def getDecodedBody(self):
		return json.loads(self.getBody(), self.getEncoding())


class etagBook(object):
	def __init__(self, id):
		id = int(id)
		self.uri = settings.ETAG_BOOK_URI%(id,)
		self.__resource = etagResource(self.uri)
		self.__resource.execute()

	def getResource(self):
		return self.__resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def get(self):
		self.__resource = etagResource(self.uri)
		self.__resource.execute()
		return self.getObject()

	def post(self, obj):
		None # TODO

	def put(self, obj):
		None # TODO

	def delete(self):
		r = etagResource(self.uri, 'delete')
		r.execute({'If-Match':self.getResource().getEtag()})
		self.getResource().set_result(r)
		return self.getObject()

