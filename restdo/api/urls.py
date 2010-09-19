# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import BookHandler

book_handler = Resource(BookHandler)

urlpatterns = patterns('',
   url(r'^book/(?P<book_slug>[^/]+)/', book_handler, { 'emitter_format': 'json' }),
)