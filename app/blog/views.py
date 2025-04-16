from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, BlogPost, Comment
from .serializers import (
    CategorySerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, CommentSerializer
)
from .permissions import IsAdminOrAlumni, IsCommentAuthor, IsPostAuthorOrReadOnly

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can manage categories
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# BlogPost Views
class BlogPostList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAlumni]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAlumni]


class BlogPostPublish(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAlumni]
    
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        post.publish()
        return Response({'status': 'post published'})


class BlogPostAddComment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Comment Views
class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        # Only allow authors or admins to update/delete comments
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser() | 
                   (permissions.IsAuthenticated() & IsCommentAuthor())]
        return [permissions.IsAuthenticated()]


class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user