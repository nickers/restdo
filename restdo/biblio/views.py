# -*- coding: utf-8 -*-

from models import etagBook, ResourceNotFound, RequestFailed
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from biblio.models import etagBooksList, etagReader, etagReadersList, etagReadersList, etagLendsList, etagLend, etagQueueList
from django.core.urlresolvers import reverse
import simplejson as json
import time



### BOOKS ###

def show_book(request, book_id):
	book = etagBook(book_id)
	#return HttpResponse(book.getResource().getBody())
	return render_to_response('biblio/book.html', {'book':book.getObject()})

def delete_book(request, book_id):
	try:
		book = etagBook(book_id)
		book.delete()
		return HttpResponseRedirect(reverse('lista_ksiazek', args=[0]))
	except ResourceNotFound:
		return HttpResponse("Resource not found", status=404)
	except:
		raise
		return HttpResponse("Strange error", status=500)



def list_books(request, page):
	page = int(page)
	obj = None
	try:
		books = etagBooksList(page)
		obj = books.getObject()
	except:
		print "Ups... some error at listing books"
	return render_to_response('biblio/books_list.html', {'books':obj, 'page':page})

def edit_book(request, id):
	if request.method=="POST":
		obj = request.POST
		if id=="":
			id = etagBook.createNewId()
			r = etagBook(id, 'get', run=False)
		else:
			id=int(id)
			r = etagBook(id, 'get')
		r.put(obj)
		return HttpResponseRedirect(reverse('edytuj_ksiazke', args=[id]))

	print "Id: [%s]"%(id,)
	if id=="":
		obj = {}
	else:
		r = etagBook(int(id))
		obj = r.getObject()
	return render_to_response('biblio/book_edit.html', {'book':obj})

### READERS ###
def delete_reader(request, reader_id):
	try:
		r = etagReader(reader_id)
		r.delete()
		return HttpResponseRedirect(reverse('lista_czytelnikow', args=[0]))
	except ResourceNotFound:
		return HttpResponse("Resource not found", status=404)
	except:
		raise
		return HttpResponse("Strange error", status=500)



def list_readers(request, page):
	page = int(page)
	obj = None
	try:
		r = etagReadersList(page)
		obj = r.getObject()
	except:
		print "Ups... some error at listing books"
	return render_to_response('biblio/readers_list.html', {'readers':obj, 'page':page})

def edit_reader(request, id):
	if request.method=="POST":
		obj = request.POST
		if id=="":
			id = etagReader.createNewId()
			r = etagReader(id, 'get', run=False)
		else:
			id=int(id)
			r = etagReader(id, 'get')
		r.put(obj)
		return HttpResponseRedirect(reverse('edytuj_czytelnika', args=[id]))

	print "Id: [%s]"%(id,)
	if id=="":
		obj = {}
	else:
		r = etagReader(int(id))
		obj = r.getObject()
	return render_to_response('biblio/reader_edit.html', {'reader':obj})

### LENDS ###
def delete_lend(request, lend_id):
	try:
		r = etagLend(lend_id)
		r.delete()
		return HttpResponseRedirect(reverse('lista_wypozyczen', args=[0]))
	except ResourceNotFound:
		return HttpResponse("Resource not found", status=404)
	except:
		raise
		return HttpResponse("Strange error", status=500)



def list_lends(request, page):
	page = int(page)
	obj = None
	try:
		r = etagLendsList(page)
		obj = r.getObject()
	except:
		print "Ups... some error at listing books"
	return render_to_response('biblio/lends_list.html', {'lends':obj, 'page':page})

def edit_lend(request, id):
	try:
		if request.method=="POST":
			obj = {}
			for k in request.POST:
				obj[k] = request.POST[k]

			for k in ['request_time','lend_time','return_time']:
				if obj[k]=="":
					obj[k] = None

			if id=="":
				id = etagLend.createNewId()
				r = etagLend(id, 'get', run=False)
			else:
				id=int(id)
				r = etagLend(id, 'get')
			r.put(obj)
			return HttpResponseRedirect(reverse('edytuj_wypozyczenie', args=[id]))

		print "Id: [%s]"%(id,)
		if id=="":
			obj = {}
		else:
			r = etagLend(int(id))
			obj = r.getObject()
		return render_to_response('biblio/lend_edit.html', {'lend':obj})
	except RequestFailed, e:
		info = json.loads(e.message)
		return render_to_response('biblio/request_failed.html', {'info':info})

def lend_mod(id, k, v):
	r = etagLend(int(id))
	obj = r.getObject()
	for id_field in ['book','reader']:
		obj[id_field] = obj[id_field]['id']
	obj[k] = v
	print obj
	r.put(obj)

def grant_lend(request, id, page):
	try:
		lend_mod(int(id), 'lend_time', time.strftime("%Y-%m-%d %H:%M:%S"))
		return HttpResponseRedirect(reverse('lista_wypozyczen', args=[page]))
	except RequestFailed, e:
		info = json.loads(e.message)
		return render_to_response('biblio/request_failed.html', {'info':info})

def grant_lend_book(request, id, book):
	try:
		lend_mod(int(id), 'lend_time', time.strftime("%Y-%m-%d %H:%M:%S"))
		return HttpResponseRedirect(reverse('kolejka_pokaz', args=[book]))
	except RequestFailed, e:
		info = json.loads(e.message)
		return render_to_response('biblio/request_failed.html', {'info':info})

def return_lend(request, id, page):
	try:
		lend_mod(int(id), 'return_time', time.strftime("%Y-%m-%d %H:%M:%S"))
		return HttpResponseRedirect(reverse('lista_wypozyczen', args=[page]))
	except RequestFailed, e:
		info = json.loads(e.message)
		return render_to_response('biblio/request_failed.html', {'info':info})

def return_lend_book(request, id, book):
	try:
		lend_mod(int(id), 'return_time', time.strftime("%Y-%m-%d %H:%M:%S"))
		return HttpResponseRedirect(reverse('kolejka_pokaz', args=[book]))
	except RequestFailed, e:
		info = json.loads(e.message)
		return render_to_response('biblio/request_failed.html', {'info':info})

### QUEUE ###
def queue_list_books(request, page):
	page = int(page)
	obj = None
	try:
		books = etagBooksList(page)
		obj = books.getObject()
	except:
		print "Ups... some error at listing books"
	return render_to_response('biblio/queue_books_list.html', {'books':obj, 'page':page})

def queue_show(request, book_id):
	book_id = int(book_id)
	try:
		lends = etagQueueList(book_id)
		obj = lends.getObject()
	except:
		print "Ups... some error at listing book's #%s lends queue"%(book_id,)
	return render_to_response('biblio/queue_show.html', {'lends':obj})

def queue_delete(request, book, id):
	book = int(book)
	id = int(id)
	try:
		lends = etagQueueList(book)
		lends.delete(id)
	except:
		print "Ups... some error at deleting book's #%s lend item #%s"%(book,id)
		raise
	return HttpResponseRedirect(reverse('kolejka_pokaz', args=[book]))
