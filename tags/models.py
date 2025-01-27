from django.db import models

# Create your models here.
class TagManager(models.Model):
    tags = models.JSONField(default=list)
    
    @classmethod
    def get_instance(cls):
        return cls.objects.get_or_create(id=1)[0]

class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

class Annotators(models.Model):
    ID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
