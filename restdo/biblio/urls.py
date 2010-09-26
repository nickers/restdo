# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
	url(r'^book/(?P<book_id>[0-9]+)$', 'biblio.views.show_book'),
	url(r'^edit_book/(?P<id>[0-9]*)$', 'biblio.views.edit_book', name='edytuj_ksiazke'),
	url(r'^book-delete/(?P<book_id>[0-9]+)$', 'biblio.views.delete_book'),
	url(r'^list_books/(?P<page>[0-9]+)$', 'biblio.views.list_books', name='lista_ksiazek'),
	#url(r'^book/page-(?P<page_number>[0-9]+)$', books_list_handler, { 'emitter_format': 'json'}),
)
