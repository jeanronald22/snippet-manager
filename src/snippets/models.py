from django.contrib.auth.models import User
from django.db import models


class Language(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="languages")
    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=10)  # Ex: "#FF5733"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="snippets")
    name = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=200)
    code = models.TextField()
    instruction = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="snippets")
    tags = models.ManyToManyField(Tag, related_name="snippets")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True, related_name="snippets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
