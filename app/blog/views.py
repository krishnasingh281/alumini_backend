from rest_framework import viewsets, permissions, filters, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, BlogPost, Comment
from .serializers import (
    CategorySerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, CommentSerializer
)


class IsAdminOrAlumni(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"User role: {getattr(request.user, 'role', None)}")
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return (
            request.user.is_authenticated and 
            request.user.role in ['admin', 'alumni']
        )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can manage categories
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'published_at']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAlumni]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.publish()
        return Response({'status': 'post published'})
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)