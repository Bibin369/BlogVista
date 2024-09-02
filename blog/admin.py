from django.contrib import admin
from .models import Comment, Post
from .models import Contact
from .models import Update

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Update)
