from django.contrib import admin
from django.urls import path, include
from olcha.views import CategoryListApiView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', CategoryListApiView, basename='categories')

urlpatterns = [
    path('category/', CategoryListApiView.as_view(), name='category-list'),
]