from django.contrib import admin
from .models import Recipe, Comment, Like

admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Like)

