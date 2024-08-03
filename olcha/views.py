from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from olcha.models import Category


# Create your views here.

class CategoryListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        name = [
            {
                'category_name':  category.category_name,
            }
            for category in Category.objects.all()]
        return Response(name, status=status.HTTP_201_CREATED)
