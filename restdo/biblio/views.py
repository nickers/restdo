# -*- coding: utf-8 -*-

from models import etagBook, ResourceNotFound
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from biblio.models import etagBooksList, etagReader, etagReadersList, etagReadersList
from django.core.urlresolvers import reverse

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
