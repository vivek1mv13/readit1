# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
	title=models.CharField(max_length=150)
	authors=models.ManyToManyField("Author",related_name="books")
	review=models.TextField(blank=True,null=True)
	date_reviewed=models.DateTimeField(blank=True,null=True)
	reviewed_by = models.ForeignKey(User,blank=True,null=True,related_name="reviews")
	is_favourite=models.BooleanField(default=False,verbose_name="Favourite?")


	def __str__(self):
		return "{}  by {}".format(self.title,self.list_authors())


	def list_authors(self):
		return ",".join([author.name for author in self.authors.all()])


	def save(self,*args,**kwargs):
		if(self.review and self.date_reviewed is None):
			self.date_reviewed=now()

		super(Book,self).save(*args,**kwargs)


class Author(models.Model):
	name =models.CharField(max_length=70,help_text="use pen name not author name",unique=True)



	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('author-detail',kwargs = {'pk', self.pk})