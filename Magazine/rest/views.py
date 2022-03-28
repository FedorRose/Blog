from django.shortcuts import render
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from main.models import *
from rest.serializers import *


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CatViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CatSerializer


class CommViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    # queryset =
    serializer_class = CommentSerializer
    lookup_field = 'post'

    def get_queryset(self):
        post = self.kwargs.get('post')
        if not post:
            return Comment.objects.all()

        return Comment.objects.filter(post=post)



    # @action(methods=['get'], detail=False)
    # def get_comm(self, request, post=None):
    #     comments = Comment.objects.filter(post=post)
    #     return Response()

