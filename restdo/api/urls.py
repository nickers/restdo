# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import BookHandler

book_handler = Resource(BookHandler)

urlpatterns = patterns('',
   url(r'^book/$', book_handler, { 'emitter_format': 'json' }),
   url(r'^book/(?P<id>[^/]+)', book_handler, { 'emitter_format': 'json' }, 'books_api'),
)