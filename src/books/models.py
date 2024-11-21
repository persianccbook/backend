import uuid
from django.db import models
from django.utils import timezone
from books.managers import ReleasedManager
from users.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# TODO: clean up image when image changes

def upload_book_cover(instance, filename):
    hashed_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id)).hex
    return f"book_covers/cover-{hashed_uuid}.{filename.split('.')[-1]}"

# Create your models here.
class Genre(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
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
    cover_image = models.ImageField(upload_to=upload_book_cover, blank=True, null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def average_rating(self):
        if self.rating.exists():
            return str(self.rating.aggregate(avg_rating=Avg('rating'))['avg_rating'])
        else:
            return '0'


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

    objects = models.Manager()
    released = ReleasedManager()



class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    chapter_number = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.title}"

    class Meta:
        unique_together = ('book', 'chapter_number')
        ordering = ['chapter_number']

class Page(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='pages')
    content = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    page_number = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Page {self.page_number} of {self.chapter.title}"

    class Meta:
        unique_together = ('chapter', 'page_number')
        ordering = ['page_number']

class Rating(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='rating')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # description = models.TextField(blank=True,null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('book','user')

    def __str__(self):
        return f"{self.user} rate {self.book} {self.rating}Star(s)"