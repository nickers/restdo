# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
	(r'^book/(?P<book_id>[0-9]+)$', 'biblio.views.show_book'),
	#url(r'^book/page-(?P<page_number>[0-9]+)$', books_list_handler, { 'emitter_format': 'json'}),
)
