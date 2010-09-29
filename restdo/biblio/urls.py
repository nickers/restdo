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

	url(r'^edit_lend/(?P<id>[0-9]*)$', 'biblio.views.edit_lend', name='edytuj_wypozyczenie'),
	url(r'^lend_delete/(?P<lend_id>[0-9]+)$', 'biblio.views.delete_lend', name="usun_wypozyczenie"),
	url(r'^list_lends/(?P<page>[0-9]+)$', 'biblio.views.list_lends', name='lista_wypozyczen'),
	url(r'^grant_lend/(?P<page>[0-9]+)/(?P<id>[0-9]+)$', 'biblio.views.grant_lend', name='daj_wypozyczenie'),
	url(r'^grant_lend/book-(?P<book>[0-9]+)/(?P<id>[0-9]+)$', 'biblio.views.grant_lend_book', name='daj_wypozyczenie_book'),
	url(r'^return_lend/(?P<page>[0-9]+)/(?P<id>[0-9]+)$', 'biblio.views.return_lend', name='zwroc_wypozyczenie'),
	url(r'^return_lend/book-(?P<book>[0-9]+)/(?P<id>[0-9]+)$', 'biblio.views.return_lend_book', name='zwroc_wypozyczenie_book'),

	url(r'^queue_books/$', 'biblio.views.queue_list_books', kwargs={'page':0}, name='kolejka_lista_ksiazek_menu'),
	url(r'^queue_books/(?P<page>[0-9]+)$', 'biblio.views.queue_list_books', name='kolejka_lista_ksiazek'),
	url(r'^queue/(?P<book_id>[0-9]+)$', 'biblio.views.queue_show', name='kolejka_pokaz'),
	url(r'^queue/(?P<book>[0-9]+)/(?P<id>[0-9]+)$', 'biblio.views.queue_delete', name='kolejka_usun'),


	url(r'^listable/(?P<type>[^/]+)/(?P<page>[0-9]+)$', 'biblio.views.choose_listable', name='listowalne'),
)
