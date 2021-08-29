from django.contrib import admin
from django.db.models.query import prefetch_related_objects
from .models import Profile,User,Post
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)



