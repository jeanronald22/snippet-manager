from rest_framework import serializers

from .models import Category, Language, Snippet, Tag


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'user', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'user', 'name', 'description', 'color', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'user', 'name', 'description', 'code', 'instruction', 'categories', 'tags', 'language',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
