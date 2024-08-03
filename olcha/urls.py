from django.urls import path
from views import CategoryListApiView

urlpatterns = [
    path('category/', CategoryListApiView.as_view(), name='category-list'),
]