# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import BookHandler, BooksListHandler, BookLendHandler, BookLendsListHandler, ReaderHandler, ReadersListHandler

book_handler = Resource(BookHandler)
books_list_handler = Resource(BooksListHandler)

book_lend_handler = Resource(BookLendHandler)
book_lends_list_handler = Resource(BookLendsListHandler)

reader_handler = Resource(ReaderHandler)
readers_list_handler = Resource(ReadersListHandler)

urlpatterns = patterns('',
   url(r'^book/page-(?P<page_number>[0-9]+)$', books_list_handler, { 'emitter_format': 'json'}),
   url(r'^book/id-(?P<id>[^/]+)$', book_handler, { 'emitter_format': 'json' }, 'books_api'),

   url(r'^lend/page-(?P<page_number>[0-9]+)$', book_lends_list_handler, { 'emitter_format': 'json'}),
   url(r'^lend/id-(?P<id>[^/]+)$', book_lend_handler, { 'emitter_format': 'json' }, 'lends_api'),

   url(r'^reader/page-(?P<page_number>[0-9]+)$', readers_list_handler, { 'emitter_format': 'json'}),
   url(r'^reader/id-(?P<id>[^/]+)$', reader_handler, { 'emitter_format': 'json' }, 'reader_api'),
)