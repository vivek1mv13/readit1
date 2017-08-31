# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Book,Author

@admin.register(Book)
class Bookadmin(admin.ModelAdmin):
	fieldsets =[
		("Book details",{"fields":["title","authors"]}),
		("Review",{"fields":["is_favourite","review","reviewed_by","date_reviewed"]}),
	]
	readonly_fields =["date_reviewed"]

	def book_authors(self,obj):
		return obj.list_authors()

	book_authors.short_description = "Author(s)"	

	list_display=("title","book_authors","date_reviewed","is_favourite",)
	list_editable =("is_favourite",)
	list_display_links =("title","date_reviewed",)
	list_filter =("is_favourite",)
	search_fields = ("title","authors__name",)

admin.site.register(Author)
#admin.site.register(Book,Bookadmin)