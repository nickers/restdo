# -*- coding: utf-8 -*-
from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	pub_date = models.DateField("publication date")