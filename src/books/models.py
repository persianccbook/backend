from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.
class Genre(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    STATUS_CHOICES = (
        ('d','draft'),
        ('p','pending'),
        ('r','released'),
    )
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(User, related_name='authored_books')
    created = models.DateField(auto_now_add=True)
    published = models.DateField(default=timezone.now)
    updated = models.DateField(auto_now=True)
    genre = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']