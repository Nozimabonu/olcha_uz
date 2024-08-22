from django.urls import path
from post import views

# from post.views import PostViewSet
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('CRUD posts', PostViewSet, basename='post')
#
# urlpatterns = [
#                   path('post-list/', views.PostApiView.as_view()),
#                   path('post-actions/', views.PostModelAPi.as_view()),
#                   path('post-detail/<int:pk>/', views.PostDetailAPiView.as_view())
#               ] + router.urls


urlpatterns = [
    path('post-list/', views.PostApiView.as_view()),
    path('post-list/<int:pk>', views.PostDetailApiView.as_view())
]
