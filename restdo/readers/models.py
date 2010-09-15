# -*- coding: utf-8 -*-
from django.db import models

class Reader(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.TextField(blank=True)
