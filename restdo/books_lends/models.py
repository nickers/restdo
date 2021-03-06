# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals
from books.models import Book
from readers.models import Reader

def book_pre_delete_signal(**kwargs):
	if 'sender' in kwargs:
		inst = kwargs['instance']
		BookLend.objects.filter(book=inst.id).delete()

def reader_pre_delete_signal(**kwargs):
	if 'sender' in kwargs:
		inst = kwargs['instance']
		BookLend.objects.filter(reader=inst.id).delete()

signals.pre_delete.connect(book_pre_delete_signal, sender=Book)
signals.pre_delete.connect(reader_pre_delete_signal, sender=Reader)

class BookLend(models.Model):
	book = models.ForeignKey('books.Book', null=True, blank=True)
	reader = models.ForeignKey('readers.Reader', null=True, blank=True)
	request_time = models.DateTimeField('lend request date', null=True, blank=True)
	lend_time = models.DateTimeField('lend date', null=True, blank=True)
	return_time = models.DateTimeField('returns date', null=True, blank=True)

	def __unicode__(self):
		if self.isEmpty():
			return u"(empty)"
		return u"[%s], by:%s[%s] -> from '%s' to '%s'"%(self.book, self.reader, self.request_time, self.lend_time, self.return_time)

	def isEmpty(self):
		attrs = ['book','reader','request_time']
		for a in attrs:
			if getattr(self, a)==None:
				return True
		return False

	@staticmethod
	def notEmptyFilter():
		return {'book__isnull':False, 'reader__isnull':False, 'request_time__isnull':False}