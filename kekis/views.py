from kekis.models import *
from kekis.serializers import *
from rest_framework import generics, response
from django.contrib.auth.models import User
from .serializers import NewSerializer, NewDetailSerializer, UserSerializer, UserDetailSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .permissions import IsCreator, IsAdmin
from django_filters import rest_framework as filters


class CustomViewSet(viewsets.ModelViewSet):

    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsCreator]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = []

        return super().get_permissions()


class CommentViewSet(CustomViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):

        if 'note' not in self.request.query_params.keys():
            return Response({'error': "Произошла ошибка"}, status=400)

        return super().list(request, *args, **kwargs)

    def get_queryset(self):

        note = self.request.query_params['note']

        queryset = super().get_queryset().filter(commented_note=note)
        return queryset
    
    
class NewsViewSet(CustomViewSet):
    
    queryset = New.objects.all()
    serializer_class = NewSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = NewDetailSerializer
        return super(NewsViewSet, self).retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        new_or_comment = self.get_object()
        new_or_comment.likes += 1
        new_or_comment.save()

        return response.Response('Liked')

    @action(detail=True, methods=['POST'])
    def dislike(self, request, pk):
        new_or_comment = self.get_object()
        new_or_comment.delete_like()
        new_or_comment.save()

        return response.Response('Disliked')
    #
    # def get_queryset(self):
    #
    #     if self.request.user.is_superuser:
    #         return super().get_queryset()
    #
    #     queryset = super().get_queryset().filter(creator=self.request.user)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)


class UserViewSet(CustomViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserDetailSerializer
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
