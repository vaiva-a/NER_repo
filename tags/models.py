from django.db import models


class TagManager(models.Model):
    tags = models.JSONField(default=list)  # Ensures an empty list if not initialized
    tags_med = models.JSONField(default=list)  # Ensures an empty list if not initialized

    @classmethod
    def get_instance(cls):
        return cls.objects.get_or_create(id=1)[0]  # Try to fetch the existing instance

class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    last_login = models.DateTimeField(null=True, blank=True)

class Annotators(models.Model):
    ID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)