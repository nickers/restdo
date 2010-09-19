# -*- coding: utf-8 -*-
from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=250)
	pub_date = models.DateField("publication date")
	slug = models.SlugField(max_length=300, unique=True)
	
	def __unicode__(self):
		return u'"%s", %s [%s]'%(self.title, self.author, self.slug)