from rest_framework import generics
from olcha.models import Group
from olcha.serializers import GroupModelSerializer


class GroupCreateApiView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer


class GroupListApiView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Group.objects.all()
        queryset = queryset.select_related('category')
        return queryset


# class GroupListApiView(APIView):
#     def get(self, request, format=None):
#         groups = Group.objects.all()
#         serializer = GroupModelSerializer(groups, many=True, context={'request': request})
#         return Response(serializer.data, status=HTTP_200_OK)

class GroupDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()

    serializer_class = GroupModelSerializer
    lookup_field = 'slug'
