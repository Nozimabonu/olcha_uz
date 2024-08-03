from rest_framework import generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .models import Category
from .serializers import CategoryModelSerializer
# Create your views here.

class CategoryListApiView(generic.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
