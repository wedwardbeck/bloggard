from django.urls import reverse_lazy
from rest_framework import generics, viewsets
from vanilla import CreateView, DeleteView, ListView, UpdateView

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ListPosts(ListView):
    model = Post


class CreatePost(CreateView):
    model = Post
    success_url = reverse_lazy('list_posts')


class EditPost(UpdateView):
    model = Post
    success_url = reverse_lazy('list_posts')


class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('list_posts')
