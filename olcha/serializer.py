from olcha.models import Category
from django.utils.text import slugify
from rest_framework import serializers


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        title = validated_data.pop('category_name', '')
        slug = slugify(title)
        validated_data['category_name'] = slug
        return Category.objects.create(**validated_data)
