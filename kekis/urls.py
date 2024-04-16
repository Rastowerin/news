from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kekis import views

router = DefaultRouter()
router.register('comments', views.CommentViewSet, basename='comment')
router.register('news', views.NewsViewSet, basename='new')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
