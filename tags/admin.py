from django.contrib import admin
from .models import TagManager, Annotators, Validators

admin.site.register(TagManager)
admin.site.register(Annotators)
admin.site.register(Validators) 
