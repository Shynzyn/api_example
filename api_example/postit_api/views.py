from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, PostLike, Comment, CommentLike
from .serializers import PostSerializer, CommentSerializer
from rest_framework.exceptions import ValidationError


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError("Negalima trinti svetimu pranesimu!")

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError("Negalima redaguoti svetimu pranesimu!")


class CommentList(generics.ListCreateAPIView):
    # queryset =  Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

