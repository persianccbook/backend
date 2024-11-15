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