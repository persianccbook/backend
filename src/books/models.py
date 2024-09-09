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
    
    def get_book_contents(self):
        chapters = self.chapters.all().order_by('chapter_number')
        chapters_with_pages = []
        for chapter in chapters:
            pages = chapter.pages.all().order_by('page_number')
            chapter_data = {
                'id': chapter.id,
                'title': chapter.title,
                'description': chapter.description,
                'chapter_number': chapter.chapter_number,
                'pages': [
                    {
                        'id': page.id,
                        'content': page.content,
                        'page_number': page.page_number
                    } for page in pages
                ]
            }
            chapters_with_pages.append(chapter_data)
        book_data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'chapters': chapters_with_pages
        }
        return book_data

    class Meta:
        ordering = ['title']



class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    chapter_number = models.IntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.title}"

    class Meta:
        ordering = ['chapter_number']

class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    content = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    page_number = models.IntegerField(unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Page {self.page_number} of {self.chapter.title}"

    class Meta:
        ordering = ['page_number']