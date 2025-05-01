from rest_framework import serializers

from .models import (
    Category, Post, Comment, Like
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.parent:
            representation['parent'] = CategorySerializer(instance.parent).data
        return representation
    
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    categories = serializers.PrimaryKeyRelatedField(
            many=True,
            queryset=Category.objects.all(),
        )    
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'categories', 'created_at', 'likes_count')

    def get_likes_count(self, obj):
        return obj.like_set.count()
    
    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        post = Post.objects.create(**validated_data)
        post.categories.set(categories_data)  
        return post
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'replies', 'parent', 'created_at')  
        read_only_fields = ('author', 'created_at')

    def create(self, validated_data):
        post_id = self.context['view'].kwargs.get('post_id')
        validated_data['post_id'] = post_id
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_replies(self, obj):
        if obj.parent is None:      
            replies = obj.replies.all()
            return CommentSerializer(replies, many=True).data
        return []

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')