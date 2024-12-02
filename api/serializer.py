from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = "__all__"


class CartoonSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    class Meta:
        model = Cartoon
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class VideoSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    cartoon = CartoonSerializer(many=False)
    class Meta:
        model = Video
        fields = ('id', 'cartoon', 'title', 'thumbnail', 'videoUrl', 'status', 'created_at', 'tags')

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]