from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from olcha.models import Product
from olcha.serializers import ProductModelSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from olcha import permissions as custom_permissions


class ProductListCreateApiView(ListCreateAPIView):
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    permission_classes = [custom_permissions.CustomPermission]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        group_slug = self.kwargs['group_slug']
        queryset = Product.objects.filter(group__category__slug=category_slug, group__slug=group_slug)
        return queryset


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [custom_permissions.CustomPermission]
    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
