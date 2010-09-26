# -*- coding: utf-8 -*-

from models import etagBook, ResourceNotFound
from django.http import HttpResponse
from django.shortcuts import render_to_response
from biblio.models import etagBooksList

def show_book(request, book_id):
	book = etagBook(book_id)
	#return HttpResponse(book.getResource().getBody())
	return render_to_response('biblio/book.html', {'book':book.getObject()})

def delete_book(request, book_id):
	try:
		book = etagBook(book_id)
		return HttpResponse(book.delete())
	except ResourceNotFound:
		return HttpResponse("Resource not found", status=404)
	except:
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
	print "Id: [%s]"%(id,)
	if id=="":
		obj = {}
	else:
		r = etagBook(int(id))
		obj = r.getObject()
	return render_to_response('biblio/book_edit.html', {'book':obj})