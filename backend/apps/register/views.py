from rest_framework import generics
from .models import Area
from .serializers import AreaSerializer
from server.protect import ProtectRelatedDeleteMixin


class AreaListCreateView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    search_fields = ['name']


class AreaUpdateDeleteView(ProtectRelatedDeleteMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'uuid'
