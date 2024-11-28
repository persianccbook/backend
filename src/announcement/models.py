from django.db import models

# Create your models here.
class Announcement(models.Model):
    id = models.AutoField(primary_key=True) 
    title = models.CharField(max_length=200) 
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['id']


class ContactUs(models.Model):
    id = models.AutoField(primary_key=True) 
    email = models.EmailField()
    message = models.TextField(max_length=2048)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Contact us'
        ordering = ['is_read','id']

    def __str__(self):
        return "ContactUs message"