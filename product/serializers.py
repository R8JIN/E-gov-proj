from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "duration_in_minutes",
            "state",
            "start_date_offset_in_minutes",
            "title",
            "price",
            "description",
            "thumbNails",
            "engine_number",
            "chassis_number",
            "datetime",
            "user",
            "category",
            "get_absolute_url",
            "get_image"
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'get_absolute_url'
        )

