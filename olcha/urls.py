from django.urls import path
# from views import CategoryListApiView
from olcha import views

urlpatterns = [
    path('category/', views.CategoryListApiView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', views.CategoryDetailApiView.as_view(), name='category-detail'),
]