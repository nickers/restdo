# -*- coding: utf-8 -*-
from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=200, null=True)
	author = models.CharField(max_length=250, null=True)
	pub_date = models.DateField("publication date", null=True)
	
	def isEmpty(self):
		return (self.title==None or self.author==None or self.pub_date==None)
	
	@staticmethod
	def notEmptyFilter():
		return {'title__isnull':False, 'author__isnull':False, 'pub_date__isnull':False}
	
	def __unicode__(self):
		return u'#%d. "%s", %s'%(self.id, self.title, self.author)