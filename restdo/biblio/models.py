# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from restkit.resource import Resource, ResourceNotFound, RequestFailed
import simplejson as json

class etagResource(object):
	def __init__(self, uri, method='get'):
		self.uri = uri
		self.method = method
		self.resource = Resource(self.uri)

	def execute(self, headers=None, body=None, ignoreErrors=False):
		try:
			self.set_result(getattr(self.resource, self.method)(headers=headers, payload=body))
		except:
			if ignoreErrors:
				self.result = None
				self.body_string = ''
			else:
				raise

	def set_result(self, r):
		self.result = r
		if callable(self.result.body_string):
			self.body_string = self.result.body_string()
		else:
			self.body_string = self.result.body_string

	def getEncoding(self):
		try:
			return self.result.charset or 'utf8'
		except:
			return 'utf8'

	def getBody(self):
		return self.body_string

	def getEtag(self):
		try:
			return self.result.headers.get('etag', None)
		except:
			return None

	def getDecodedBody(self):
		return json.loads(self.getBody(), self.getEncoding())


class etagBook(object):
	def __init__(self, id, method="get", run=True):
		if id!=None:
			id = int(id)
		self.uri = settings.ETAG_BOOK_URI%(id,)
		self._resource = etagResource(self.uri, method)
		if run:
			self._resource.execute()

	@staticmethod
	def createNewId():
		r = etagResource(settings.ETAG_BOOK_POST, 'post')
		r.execute()

		print r.result
		print r.result.headers['location']
		url = r.result.headers['location']

		import re
		p = re.compile(".*\/([0-9]+)$")
		id = p.findall(url)[0]
		return int(id)

	def getResource(self):
		return self._resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def get(self):
		self._resource = etagResource(self.uri)
		self._resource.execute()
		return self.getObject()

	def post(self, obj):
		None # TODO

	def put(self, obj):
		obj = json.dumps(obj)
		r = etagResource(self.uri, 'put')
		try:
			h = {}
			etag = self.getResource().getEtag()
			if etag!=None:
				h['If-Match'] = etag
		except:
			None
		r.execute( h, body=obj)
		return r.getBody()

	def delete(self):
		r = etagResource(self.uri, 'delete')
		r.execute({'If-Match':self.getResource().getEtag()})
		self.getResource().set_result(r)
		return self.getString()==""



class etagBooksList(etagBook):
	def __init__(self, id):
		id = int(id)
		self.uri = settings.ETAG_BOOKS_LIST_URI%(id,)
		self._resource = etagResource(self.uri)
		self._resource.execute()

	def post(self, obj):
		return None

	def put(self, obj):
		return None

	def delete(self):
		return None

## ## READERS ## ##
class etagReader(object):
	def __init__(self, id, method="get", run=True):
		if id!=None:
			id = int(id)
		self.uri = settings.ETAG_READER_URI%(id,)
		self._resource = etagResource(self.uri, method)
		if run:
			self._resource.execute()

	@staticmethod
	def createNewId():
		r = etagResource(settings.ETAG_READER_POST, 'post')
		r.execute()

		url = r.result.headers['location']

		import re
		p = re.compile(".*\/([0-9]+)$")
		id = p.findall(url)[0]
		return int(id)

	def getResource(self):
		return self._resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def get(self):
		self._resource = etagResource(self.uri)
		self._resource.execute()
		return self.getObject()

	def post(self, obj):
		None # TODO

	def put(self, obj):
		obj = json.dumps(obj)
		r = etagResource(self.uri, 'put')
		try:
			h = {}
			etag = self.getResource().getEtag()
			if etag!=None:
				h['If-Match'] = etag
		except:
			None
		r.execute( h, body=obj)
		return r.getBody()

	def delete(self):
		r = etagResource(self.uri, 'delete')
		r.execute({'If-Match':self.getResource().getEtag()})
		self.getResource().set_result(r)
		return self.getString()==""

class etagReadersList(etagReader):
	def __init__(self, id):
		id = int(id)
		self.uri = settings.ETAG_READERS_LIST_URI%(id,)
		self._resource = etagResource(self.uri)
		self._resource.execute()

	def post(self, obj):
		return None

	def put(self, obj):
		return None

	def delete(self):
		return None


## ## LENDS ## ##
class etagLend(object):
	def __init__(self, id, method="get", run=True):
		if id!=None:
			id = int(id)
		self.uri = settings.ETAG_LEND_URI%(id,)
		self._resource = etagResource(self.uri, method)
		if run:
			self._resource.execute()

	@staticmethod
	def createNewId():
		r = etagResource(settings.ETAG_LEND_POST, 'post')
		r.execute()

		url = r.result.headers['location']

		import re
		p = re.compile(".*\/([0-9]+)$")
		id = p.findall(url)[0]
		return int(id)

	def getResource(self):
		return self._resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def get(self):
		self._resource = etagResource(self.uri)
		self._resource.execute()
		return self.getObject()

	def post(self, obj):
		None # TODO

	def put(self, obj):
		obj = json.dumps(obj)
		r = etagResource(self.uri, 'put')
		try:
			h = {}
			etag = self.getResource().getEtag()
			if etag!=None:
				h['If-Match'] = etag
		except:
			None
		r.execute( h, body=obj)
		return r.getBody()

	def delete(self):
		r = etagResource(self.uri, 'delete')
		r.execute({'If-Match':self.getResource().getEtag()})
		self.getResource().set_result(r)
		return self.getString()==""

class etagLendsList(etagLend):
	def __init__(self, id):
		id = int(id)
		self.uri = settings.ETAG_LENDS_LIST_URI%(id,)
		self._resource = etagResource(self.uri)
		self._resource.execute()

	def post(self, obj):
		return None

	def put(self, obj):
		return None

	def delete(self):
		return None

### QUEUE ###
class etagQueueList(etagBook):
	def __init__(self, id):
		id = int(id)
		self.id = id
		self.uri = settings.ETAG_QUEUE_LIST_URI%(id,)
		self._resource = etagResource(self.uri)
		self._resource.execute()

	def getResource(self):
		return self._resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def delete(self, id):
		id = int(id)
		uri = settings.ETAG_QUEUE_ITEM_URI%(self.id, id)
		r = etagResource(uri, 'get')
		r.execute()
		r2 = etagResource(uri, 'delete')
		r2.execute({'If-Match':r.getEtag()})
		return r2.getBody()==""

### ### ###
class etagListables(object):
	def __init__(self, type, page):
		self.uri = settings.ETAG_LISTABLES_ITEMS_URI%(type,int(page))
		self._resource = etagResource(self.uri)
		self._resource.execute()

	def getResource(self):
		return self._resource

	def getObject(self):
		return self.getResource().getDecodedBody()

	def getString(self):
		return self.getResource().getBody()

	def get(self):
		self._resource = etagResource(self.uri)
		self._resource.execute()
		return self.getObject()
