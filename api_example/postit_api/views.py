from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response

from .models import Post, PostLike, Comment, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

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
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
        if comment.exist():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima trinti svetimu komentaru')

    def put(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError("Negalima redaguoti svetimu komentaru!")


class PostLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post, user=user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("Jus jau palaikinot sita posta")
        else:
            post = Post.objects.get(pk=self.kwargs['pk'])
            serializer.save(user=self.request.user, post=post)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("Jus nepalikote laiko po siuo postu")


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )




