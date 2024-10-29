from django.contrib import admin
from app import models

# Register your models here.

@admin.register(models.Profile)
class UserProfile(admin.ModelAdmin):
    list_display = ("name", "birth_date")

@admin.register(models.User)
class User(admin.ModelAdmin):
    list_display = ("login",)

@admin.register(models.Group)
class Group(admin.ModelAdmin):
    list_display = ("name", "admin")

@admin.register(models.Post)
class Post(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")

@admin.register(models.Comment)
class Comment(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

@admin.register(models.Item)
class Item(admin.ModelAdmin):
    list_display = ("name", "type")