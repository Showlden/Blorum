from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PostViewSet,
    CommentViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')

urlpatterns = router.urls
