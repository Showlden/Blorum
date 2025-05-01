from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Post, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'post_count')
    list_filter = ('parent',) 
    search_fields = ('name',) 

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Постов'
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category_list', 'created_at', 'like_count')
    list_filter = ('categories', 'author', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('like_count_display',)  
    filter_horizontal = ('categories',) 

    def category_list(self, obj):
        return ", ".join([c.name for c in obj.categories.all()])
    category_list.short_description = 'Категории'

    def like_count(self, obj):
        return obj.like_set.count()
    like_count.short_description = 'Лайки'

    def like_count_display(self, obj):
        return format_html("<b>{}</b>", obj.like_set.count())
    like_count_display.short_description = 'Всего лайков'
    
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('text',)
    raw_id_fields = ('parent',)  

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if 'parent' in request.GET:
            parent = Comment.objects.get(id=request.GET['parent'])
            initial['post'] = parent.post
        return initial
    
from .models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('post', 'user')
    date_hierarchy = 'created_at'  