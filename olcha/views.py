from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveDestroyAPIView
from olcha.models import Category
from olcha.serializer import CategoryModelSerializer


# Create your views here.

class CategoryListApiView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)


class CategoryDetailApiView(RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = (AllowAny,)
    search_field = 'slug'


# class CategoryListApiView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializers_class = CategoryModelSerializer(queryset, many=True)
#     permission_classes = [AllowAny]


# class CategoryDetailApiView(APIView):
#
#     def get(self, request, slug):
#         category = Category.objects.get(slug=slug)
#         serializer = CategoryModelSerializer(category)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CategoryCreateApiView(APIView):
#     def post(self, request):
#         serializer = CategoryModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response('Product Successful Create', status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CategoryUpdateApiView(APIView):
#     def get(self, request, slug):
#         category = Category.objects.get(slug=slug)
#         serializer = CategoryModelSerializer(category)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, slug):
#         category = Category.objects.get(slug=slug)
#         serializer = CategoryModelSerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
