# -*- coding: utf-8 -*-
from django.db import models

class Reader(models.Model):
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	address = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return u"%s %s"%(self.first_name, self.last_name)

	def isEmpty(self):
		attrs = ['first_name','last_name']
		for a in attrs:
			if getattr(self, a)==None:
				return True
		return False

	@staticmethod
	def notEmptyFilter():
		return {'first_name__isnull':False, 'last_name__isnull':False}