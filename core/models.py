from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name="child")

    def __str__(self):
        return self.title    


class Book(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    thumbnail = models.ImageField(upload_to = "thumbnails/")
    author = models.CharField(max_length=100)
    edition = models.CharField(max_length=20)
    posted_date = models.DateTimeField(default = timezone.now)        

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    rel = models.OneToOneField(User, on_delete=models.CASCADE)
    mob = models.CharField(max_length=20)
    branch = models.CharField(max_length=100)
    sem = models.IntegerField()
    
    def __str__(self):
        return self.rel.username


class Book_request(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(User,on_delete=models.CASCADE, related_name="reciever")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="requested_book")
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender} requested { self.reciever } for { self.book }"