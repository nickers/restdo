# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
	url(r'^book/(?P<book_id>[0-9]+)$', 'biblio.views.show_book'),
	url(r'^edit_book/(?P<id>[0-9]*)$', 'biblio.views.edit_book', name='edytuj_ksiazke'),
	url(r'^book_delete/(?P<book_id>[0-9]+)$', 'biblio.views.delete_book', name="usun_ksiazke"),
	url(r'^list_books/(?P<page>[0-9]+)$', 'biblio.views.list_books', name='lista_ksiazek'),

	url(r'^edit_reader/(?P<id>[0-9]*)$', 'biblio.views.edit_reader', name='edytuj_czytelnika'),
	url(r'^reader_delete/(?P<reader_id>[0-9]+)$', 'biblio.views.delete_reader', name="usun_czytelnika"),
	url(r'^list_readers/(?P<page>[0-9]+)$', 'biblio.views.list_readers', name='lista_czytelnikow'),

	#url(r'^book/page-(?P<page_number>[0-9]+)$', books_list_handler, { 'emitter_format': 'json'}),
)
