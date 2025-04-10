from django.urls import path
from . import views

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    
    # BlogPost URLs
    path('posts/', views.BlogPostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.BlogPostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/publish/', views.BlogPostPublish.as_view(), name='post-publish'),
    path('posts/<int:pk>/comments/', views.BlogPostAddComment.as_view(), name='post-add-comment'),
    
    # Comment URL
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
]