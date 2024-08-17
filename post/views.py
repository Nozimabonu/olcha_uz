from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostSerializer
from post import permissions as custom_permissions


# Create your views here.


# class PostApiView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostModelAPi(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#                 'success': True,
#                 'data': serializer.data
#             }
#             return Response(data=data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self):
#         pass
#
#     def delete(self):
#         pass
#
#
# class PostDetailAPiView(APIView):
#     def get(self, request, pk, format=None):
#         post = Post.objects.get(id=pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         try:
#             post = Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self):
#         pass
#
#     def delete(self):
#         pass
#
#
# class PostViewSet(ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()


class PostCreateAPIView(ListCreateAPIView):
    permission_classes = [custom_permissions.CustomPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.CustomPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
