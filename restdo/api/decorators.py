# -*- coding: utf-8 -*-

def etag_must_match(f):
	def etag_compare(self, request, *args, **kwargs):
		#print self
		print request.META
		#print dir(request)
		#print kwargs
		return f(self,request, *args, **kwargs)
	return etag_compare
		