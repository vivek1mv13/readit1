# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,DetailView
from django.shortcuts import render,get_object_or_404,redirect
from django.shortcuts import HttpResponse
from .models import Book,Author
from django.db.models import Count
from .forms import ReviewForm,BookForm
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
# Create your views here.
def list_books(request):

	"""list the books that have reviewed"""
	books =Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')
	context ={
		'books':books,
	}
	return render(request,"list.html",context)
	#return HttpResponse("we could put any thing") #request.user.username-tells username


class AuthorList(View):
	def get(self,request):

		authors=Author.objects.annotate(published_books=Count('books')).filter(published_books__gt=0)
#count the no of books associated with each author 
		context ={

		'authors':authors,
		}

		return render(request,"authors.html",context)

class BookDetail(DetailView):
	model=Book
	template_name="book.html"


class AuthorDetail(DetailView):
	model=Author
	template_name="author.html"


#def review_books(request):
class ReviewList(View):


	
	"""list all of the books that we want to review."""
	def get(self,request):
		books = Book.objects.filter(date_reviewed__isnull = True).prefetch_related('authors')
		context={
			'books':books,
			'form':BookForm,
		}
		return render(request, "list-to-review.html",context)

	def post(self,request):
		form =BookForm(request.POST)
		books = Book.objects.filter(date_reviewed__isnull = True).prefetch_related('authors')

		if form.is_valid():
			form.save()
			return redirect('review-books')

		context={
			'form':form,
			'books':books,
		}
		return render(request, "list-to-review.html",context)

@login_required
def review_book(request,pk):
	"""review an individual book"""
	book = get_object_or_404(Book,pk=pk)
	if request.method =='POST':
		#process ourform
		form=ReviewForm(request.POST)
		if form.is_valid():
			book.is_favourite =form.cleaned_data['is_favourite']
			book.review =form.cleaned_data['review']
			book.reviewed_by = request.user 
			book.save()

			return redirect('review-books')

	else:
		form=ReviewForm
	context={
		'book': book,
		'form': form,
	}
	return render(request,"review-book.html",context)

class CreateAuthor(CreateView):
	model = Author
	fields = ['name',]
	template_name = "create-author.html"

	def get_success_url(self):
		return reverse('review-books')

