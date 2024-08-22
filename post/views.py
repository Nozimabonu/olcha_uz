from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    @method_decorator(cache_page(  60))
    def get(self, request, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.select_related('author').prefetch_related('tags')
        return queryset


class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.CustomPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'


class PostApiView(APIView, PageNumberPagination):
    permission_classes = [permissions.AllowAny]
    page_size = 100

    def get(self, request, *args, **kwargs):
        cache_key = 'post-list'
        cached_data = cache.get(cache_key)  # postlani datasini oladigan cache_date
        if cached_data is None:
            cached_data = Post.objects.all()
            results = self.paginate_queryset(cached_data, request, view=self)

            serializer = PostSerializer(results, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 5)
            return self.get_paginated_response(serializer.data)
        return Response


class PostDetailApiView(APIView, PageNumberPagination):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        cache_key = f'post_detail_{post_id}'
        post_data = cache.get(cache_key)
        if not post_data:
            post_data = Post.objects.get(id=post_id)
            serializer = PostSerializer(post_data, many=False)
            cache.set(cache_key, serializer.data, timeout=60 * 3)
            return Response(serializer.data)
        return Response(post_data)


