from django.db import models

# Create your models here.
class Version(models.Model):
    link = models.CharField(max_length=255)
    release_date = models.DateField()
    update_date = models.DateField()
    md5_hash = models.CharField(max_length=32)
    
