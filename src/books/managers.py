from django.db import models

class ReleasedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="r")