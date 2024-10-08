from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from olcha.models import Category
from olcha.serializers import CategoryModelSerializer


# Create your views here.


class CategoryListApiView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryModelSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Product Successfully Created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ListOrCreate


class CategoryDetailApiView(APIView):

    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        if category:
            category.delete()
            data = {
                'data': 'Category Successfully deleted ! ',
                'status': 200
            }
            return Response(data)

    def post(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryModelSerializer(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'Category Successfully Updated',
                'status': status.HTTP_200_OK
            }
            return Response(data)


class CategoryCreateApiView(APIView):

    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Category Successfully Created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateApiView(ListAPIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data)

    def post(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryModelSerializer(data=request.data, instance=category)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'Category Successfully Updated',
                'status': status.HTTP_200_OK
            }
            return Response(data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteApiView(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data)

    def delete(self, request, slug):
        category = Category.objects.get(slug=slug)
        if category:
            category.delete()
            data = {
                'data': 'Category Successfully deleted ! ',
                'status': 200
            }
            return Response(data)
