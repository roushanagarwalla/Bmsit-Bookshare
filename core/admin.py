from django.contrib import admin
from core.models import Book,Contact,Categories, Book_request

# Register your models here.

admin.site.register(Book)
admin.site.register(Contact)
admin.site.register(Categories)
admin.site.register(Book_request)